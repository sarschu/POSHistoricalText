#!/usr/bin/env python

# -*- coding: utf-8 -*-
import sys
import codecs
import os
import ConfigParser
import datetime
import subprocess
import re
import sys
import shutil

"""
usage: python POS_tag.py <configFile> 

config file:

[Model]
modelFilePath: /path/to/model (if you have a trained model and just wanna tag)
modelOut: /out/of/new/model

[TrainParameters]
tdCutoff: Tag dictionary cutoff. Default: none.
numRawTokens: Number of raw tokens (complete sentences up to this number of total tokens). Default: infinite.
labelPropIterations: Number of iterations for the label propagation procedure. Default 200
emIterations: Number of iterations for the HMM EM training procedure. Default 50
memmIterations: Number of iterations for the MEMM training procedure. Default 100
memmCutoff: Cutoff for number of feature occurrences. Default 100

[Corpus]
rawFile= /path/to/File/to/tag
annotatedSent= /path/to/annotated/file (if you wanna train a model and tag)
annotatedType= /path/to/annotated/file (if you wanna train a model and tag)
evalFile = /path/to/eval/file (if you wanna evaluate)
outputFile = /path/to/tagged/file

[Tools]
tagger = /path/to/Tagger/run
"""
config = ConfigParser.ConfigParser()
config.optionxform = str 
config.read(sys.argv[1])

train = False
dev = False
train_param=[]
wordVecModel=''
load=False
try:
	word2embeddings=config.get('Tools','word2embeddings')
	tagger = config.get('Tools','tagger')
	rawFile= config.get('Corpus','rawFile')
	outputFile= sys.argv[4]
	raw_data = config.get('Corpus','rawFile')
	word_dict = config.get('Corpus','wordDictionary')
	train_data = sys.argv[2]
	if 'TrainParameters' in config.sections():
		for param in config.options('TrainParameters'):
			if len(param)>1:
				train_param.append('--'+param)
			else:
				train_param.append('-'+param)	
 		train_param.append(config.get('TrainParameters',param))

	if 'wordVecModel' in config.options('Model'):
		wordVecModel = config.get('Model','wordVecModel')
	if 'POSModel' in config.options('Model'):
		model = config.get('Model','POSModel') 
	else:


		train = True

	
	dev=True
	devFile= sys.argv[3]



except (ConfigParser.NoOptionError,ConfigParser.NoSectionError),e:
	print "Error: Option %s not specified in configuration file!" % e.message


sys.path.append('/'.join(word2embeddings.split('/')[:-2])+'/')
sys.path.append('/'.join(tagger.split('/')[:-1])+'/')
sys.path.append('/'.join(tagger.split('/')[:-1])+'/nlpnet/')

timestamp=datetime.datetime.now().isoformat()

outputDirectory=outputFile.split('/')[0]+'/nn_training/'+timestamp
os.mkdir(outputDirectory)
current_env = os.environ.copy()
current_env['PYTHONPATH'] = ':'.join(sys.path)

print current_env
if train:
	
	#if not given, train word embeddings	
	if wordVecModel=='':
		word2emb = subprocess.Popen(['python',word2embeddings,'--train-file',raw_data,'--vocabulary',word_dict],env=current_env)
		word2emb.communicate()
		for el in os.listdir('.'):
			if el[0:10]=='WordPhrase':
				wordVecModel=el
		shutil.copy(wordVecModel,outputDirectory)
	else:
		shutil.copy(wordVecModel,outputDirectory)
		wordVecModel=wordVecModel.split('/')[-1]
	
	shutil.copy('metadata-pos.pickle',outputDirectory)
	#load word embeddings
	load_emb= subprocess.Popen(['python',tagger+'/nlpnet-load-embeddings.py','word2embeddings',outputDirectory+'/'+wordVecModel,'-v', word_dict,'-o',outputDirectory],env=current_env)
	load_emb.communicate()
	load=True
	if train_param !=[]:
		if dev:
			args = ['python',tagger+'/nlpnet-train.py','pos']+train_param+['--gold',train_data,'--data',outputDirectory,'--dev',devFile]
		else:
			args = ['python',tagger+'/nlpnet-train.py','pos']+train_param+['--gold',train_data,'--data',outputDirectory]
		trainer = subprocess.Popen(args,env=current_env)

	else:
		print 'no additional parameters'
		if dev:
			trainer = subprocess.Popen(['python',tagger+'/nlpnet-train.py','pos','--gold',train_data,'--data',outputDirectory,'--dev',devFile],env=current_env)
		else:
			trainer = subprocess.Popen(['python',tagger+'/nlpnet-train.py','pos','--gold',train_data,'--data',outputDirectory],env=current_env)
	out,err=trainer.communicate()
	print err



if not load:
	shutil.copy(wordVecModel,'data/'+timestamp)
	modeldir='/'.join(wordVecModel.split('/')[:-1])
	wordVecModel=wordVecModel.split('/')[-1]	
	load_emb= subprocess.Popen(['python',tagger+'/nlpnet-load-embeddings.py','word2embeddings',outputDirectory+'/'+wordVecModel,'-v', word_dict,'-o','data/'+timestamp],env=current_env)
	load_emb.communicate()

	shutil.copy(model,outputDirectory)
	shutil.copy(modeldir+'/metadata-pos.pickle',outputDirectory)
	shutil.copy(modeldir+'/pos-tags.txt',outputDirectory)
	shutil.copy(modeldir+'/types-features.npy',outputDirectory)
	shutil.copy(modeldir+'/vocabulary.txt',outputDirectory)


rawin = codecs.open(raw_data,'r')
out=codecs.open(outputFile+'_tmp','w')
tagger = subprocess.Popen(['python',tagger+'/nlpnet-tag.py','pos','--data',outputDirectory,'-t'],stdin=rawin,stdout=out,env=current_env)
tagger.wait()


taggedFile= codecs.open(outputFile+'_tmp','r').read()
finalFile= codecs.open(outputFile,'w')
typeDict={}
annotFile = codecs.open(train_data,'r').read()
annotatedTokens = annotFile.split() 

for token in annotatedTokens:
	t,p=token.split('_')
	if t in typeDict:
		if p.strip() not in typeDict[t]:
			typeDict[t].append(p.strip())
	else:
		if t != '[':
			typeDict[t]=[p.strip()]

for ty in typeDict:
	if len(typeDict[ty]) == 1:
		if ty == '.':
			regex=r'\.\_'+'[^ \n]*'
			replace=r'._'+typeDict[ty][0]
		elif ty == ')':
			regex=r'\)\_'+'[^ \n]*'
			replace=r')_'+typeDict[ty][0]
		elif ty == '(':
			regex=r'\(\_'+'[^ \n]*'
			replace=r'(_'+typeDict[ty][0]
		elif ty == '?':
			regex=r'\?\_'+'[^ \n]*'
			replace=r'?_'+typeDict[ty][0]
		else:
			regex=ty+r'\_'+'[^ \n]*'
			replace=ty+r'_'+typeDict[ty][0]
			
		taggedFile = re.sub(regex,replace,taggedFile)

taggedTokens = taggedFile.split(' ')
#adj
lich='li(g|ch)(e|en|es|er|em)*\_'
tze='tze(r|s|m)\_'
haft='[^(be|c)]haft(en|er|es|en)*\_'
sam='sam\_'
ig='(d|t|z)ig\_'
isch= 'isch(en|em|es)'
bar = 'bar\_'
#nomen
hait = 'hait\_'

#verben
participle='ge[^ ]*(t|d)\_'
participle2='ge[^ ]{2,}n\_'
ver='ver[^\_]{3,}\_'
print taggedTokens
for i,tok in enumerate(taggedTokens):
	toks=tok.split('\n')
	for p,t in enumerate(toks):
		if (re.match(participle,t)!= None and t.split('_')[1]!='NA') or (re.match(participle2,t)!= None and t.split('_')[1]!='NA'):
			toks[p] = re.sub('\_.*','_VV',t)
		if re.match(ver,t)!= None:
			toks[p] = re.sub('\_.*','_VV',t)
		if re.search(lich,t) != None or re.search(tze,t) != None or re.search(haft,t) != None or re.search(ig,t) != None or re.search(bar,t) != None or re.search(isch,t) != None:
			toks[p] = re.sub('\_.*','_ADJ',t)

		if re.search(hait,t) != None:
			toks[p] = re.sub('\_.*','_NA',t)
	taggedTokens[i]='\n'.join(toks)


				
	
finalFile.write(' '.join(taggedTokens))
#os.remove(outputFile+'_tmp')
		
shutil.move(outputFile+'_tmp',outputFile+'_withoutRules')

