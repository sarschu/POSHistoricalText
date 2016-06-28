#!/usr/bin/env python

# -*- coding: utf-8 -*-
import sys
import codecs
import os
import ConfigParser
import datetime
import subprocess
import re
import json
import operator
import sys
import shutil
import uuid
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
outGiven=False
batchSize=''
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
	indices= json.load(open(sys.argv[5]))


except (ConfigParser.NoOptionError,ConfigParser.NoSectionError),e:
	print "Error: Option %s not specified in configuration file!" % e.message


sys.path.append('/'.join(word2embeddings.split('/')[:-2])+'/')
sys.path.append('/'.join(tagger.split('/')[:-1])+'/')
sys.path.append('/'.join(tagger.split('/')[:-1])+'/nlpnet/')

timestamp=datetime.datetime.now().isoformat()

outdir=outputFile.split('/')[0]+'/nn_training/'+timestamp
os.mkdir(outdir)
if dev:
	acc_log = codecs.open(outdir+'/accuracy','w','utf8')
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
		shutil.copy(wordVecModel,outdir)
	else:
		shutil.copy(wordVecModel,outdir)
		wordVecModel=wordVecModel.split('/')[-1]
	
	shutil.copy('metadata-pos.pickle',outdir)
	#load word embeddings
	load_emb= subprocess.Popen(['python',tagger+'/nlpnet-load-embeddings.py','word2embeddings',outdir+'/'+wordVecModel,'-v', word_dict,'-o',outdir],env=current_env)
	load_emb.communicate()
	load=True
	if train_param !=[]:
		if dev:
			args = ['python',tagger+'/nlpnet-train.py','pos']+train_param+['--gold',train_data,'--data',outdir,'--dev',devFile]
		else:
			args = ['python',tagger+'/nlpnet-train.py','pos']+train_param+['--gold',train_data,'--data',outdir]
		trainer = subprocess.Popen(args,env=current_env)

	else:
		print 'no additional parameters'
		if dev:
			trainer = subprocess.Popen(['python',tagger+'/nlpnet-train.py','pos','--gold',train_data,'--data',outdir,'--dev',devFile],env=current_env)
		else:
			trainer = subprocess.Popen(['python',tagger+'/nlpnet-train.py','pos','--gold',train_data,'--data',outdir],env=current_env)
	out,err=trainer.communicate()
	print err



if not load:
	shutil.move(wordVecModel,outdir)
	modeldir='/'.join(wordVecModel.split('/')[:-1])
	wordVecModel=wordVecModel.split('/')[-1]	
	load_emb= subprocess.Popen(['python',tagger+'/nlpnet-load-embeddings.py','word2embeddings',outdir+'/'+wordVecModel,'-v', word_dict,'-o',outdir],env=current_env)
	load_emb.communicate()

	shutil.copy(model,outdir)
	shutil.copy(modeldir+'/metadata-pos.pickle',outdir)
	shutil.copy(modeldir+'/pos-tags.txt',outdir)
	shutil.copy(modeldir+'/types-features.npy',outdir)
	shutil.copy(modeldir+'/vocabulary.txt',outdir)


rawin = codecs.open(raw_data,'r')
tmp_file = str(uuid.uuid4())
out=codecs.open(tmp_file,'w','utf8')
tagger_p = subprocess.Popen(['python',tagger+'/nlpnet-tag.py','pos','--data',outdir,'-t','--prob'],stdin=rawin,stdout=out,env=current_env)
tagger_p.wait()
out.close()
if dev:
	dev_part_pred=[]
	tf = codecs.open(tmp_file,'r','utf8').readlines()#index of dev output in tmp file with probs
	tf2=[]
	for l in range(0,len(tf),2):
		tf2.append(tf[l])
	for ind in indices['dev']:
		dev_part_pred.append(tf2[ind])
		
	print dev_part_pred
	dF= codecs.open(devFile,'r','utf8').read()
	gold=dF.split()
	pred=[]
	for line in range(0,len(dev_part_pred)):
		pred = pred+dev_part_pred[line].split()
	found=0
	print len(gold)
	print gold
	print len(pred)
	print pred
	for ind,el in enumerate(gold):
		g= el.split('_')[1]
		p= pred[ind].split('_')[1]
		if g.strip()==p.strip():
			found+=1
	print 'accuracy'
	acc= float(found)/float(len(gold))
	print acc
	acc_log.write('Accuracy iteration 0 : '+str(acc)+'\n')
###selftraining###

# here the criterion for a sentence to be added to the train data is hidden
# batch size amount of sentences added to train
# batch size highest scoring viterbi scores from the neural net. normalized by sentence length
def add_train_data(probdict,train_data,iteration_folder,batch_size=200):
	sorted_probdict = sorted(probdict.items(), key=operator.itemgetter(1))
	additional_train=[]
	store_probdict_entries={}

	if len(sorted_probdict)> batch_size: 
		print 'this case'
		for sent in sorted_probdict[-batch_size:]:
			additional_train.append(sent[0])
			store_probdict_entries[sent]= probdict[sent[0]]
			del probdict[sent[0]]

	else:
		for sent in sorted_probdict:
			additional_train.append(sent[0])
			store_probdict_entries[sent]= probdict[sent[0]]
			del probdict[sent[0]]
	add_t_tmp = str(uuid.uuid4())

	add_train=codecs.open(add_t_tmp,'w','utf8')
	for line in additional_train:
		add_train.write(line)
	add_train.close()
	new_train=codecs.open(iteration_folder+'/train','w','utf8')
	cat = subprocess.Popen(['cat',train_data,add_t_tmp],stdout=new_train)
	cat.communicate()
	os.remove(add_t_tmp)
	new_train.close()
	return store_probdict_entries

def adjust_probs(taggedFile, dictionary,iteration):

	for sent in range(0,len(taggedFile)-2,2):
		if iteration == 1:
			dictionary[taggedFile[sent]]=float(taggedFile[sent+1].strip())
		else:
			if taggedFile[sent] in dictionary:
				dictionary[taggedFile[sent]]=float(taggedFile[sent+1].strip())
				
#while dict ={}
#train_data=train_data+10% best scoring
#pop these out of dict
#update dict with new probs

### exists by that time in any case: wordVecModel

probdict={}
do_self_training=True
accuracy_last=0.0

iteration=1
ac_development=[]
tmp_f_names=[]
while do_self_training==True:

	print iteration
	iter_folder= outdir+'/iter'+str(iteration)
	os.mkdir(iter_folder)
	taggedFile= codecs.open(tmp_file,'r','utf8').readlines()[526:]
	print taggedFile[:6]
	adjust_probs(taggedFile,probdict,iteration)

	if batchSize !='':
		add_train_data(probdict,train_data,iter_folder,batch_size=batchSize)
	else:
		add_train_data(probdict,train_data,iter_folder)
	train_data=iter_folder+'/train'
	if train_param !=[]:
		if dev:
			args = ['python',tagger+'/nlpnet-train.py','pos']+train_param+['--gold',train_data,'--data',iter_folder,'--dev',devFile]
		else:
			args = ['python',tagger+'/nlpnet-train.py','pos']+train_param+['--gold',train_data,'--data',iter_folder]
		trainer = subprocess.Popen(args,env=current_env)
	else:
		trainer = subprocess.Popen(['python',tagger+'/nlpnet-train.py','pos','--gold',train_data,'--data',iter_folder],env=current_env)
	trainer.communicate()

	modeldir='/'.join(wordVecModel.split('/')[:-1])
	wordVecModel=wordVecModel.split('/')[-1]	
	load_emb= subprocess.Popen(['python',tagger+'/nlpnet-load-embeddings.py','word2embeddings',outdir+'/'+wordVecModel,'-v', word_dict,'-o',outdir+'/iter'+str(iteration)],env=current_env)
	load_emb.communicate()


	rawin = codecs.open(raw_data,'r')
	
	os.remove(tmp_file)
	tmp_file= str(uuid.uuid4())
	out=codecs.open(tmp_file,'w','utf8')
	tagger_p = subprocess.Popen(['python',tagger+'/nlpnet-tag.py','pos','--data',iter_folder,'-t','--prob'],stdin=rawin,stdout=out,env=current_env)
	tagger_p.wait()
	out.close()
	if probdict =={}:
		do_self_training = False
	shutil.copy(tmp_file,iter_folder)
	#give an impression how accuracy develops over time during the self training process
	if dev:

		dev_part_pred=[]
		tf = codecs.open(tmp_file,'r','utf8').readlines()#index of dev output in tmp file with probs
		tf2=[]
		for l in range(0,len(tf),2):
			tf2.append(tf[l])
		for ind in indices['dev']:
			dev_part_pred.append(tf2[ind])
		
		print dev_part_pred
		dF= codecs.open(devFile,'r','utf8').read()
		gold=dF.split()
		pred=[]
		found=0
		for line in range(0,len(dev_part_pred)):
			pred = pred+dev_part_pred[line].split()
		for ind,el in enumerate(gold):
			g= el.split('_')[1]
			p= pred[ind].split('_')[1]
			if g.strip()==p.strip():
				found+=1
		print 'accuracy'
		acc = float(found)/float(len(gold))
		ac_development.append(acc)
		tmp_f_names.append(tmp_file)
		if accuracy_last >= acc:

			shutil.copy(outdir+'/iter'+str(iteration-1)+'/train',iter_folder)
		else:	
			acc_log.write('Added training data because '+str(acc)+' is higher than'+str(accuracy_last)+'\n')
			accuracy_last = acc

		print acc
		acc_log.write('Accuracy iteration '+str(iteration) +' : ' +str(acc)+'\n')
		
	iteration+=1		
acc_log.close()
final=codecs.open(outputFile,'w','utf8')
#tmp=codecs.open(tmp_file,'r','utf8').readlines()
best_iter = ac_development.index(max(ac_development))
tmp=codecs.open(outdir+'/iter'+str(best_iter+1)+'/'+tmp_f_names[best_iter],'r','utf8').readlines()
for line in range(0,len(tmp)-2,2):
	final.write(tmp[line])
os.remove(tmp_file)
final.close()
	
