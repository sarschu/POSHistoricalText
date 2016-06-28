#!/usr/bin/python
# -*- coding: utf8 -*-

import codecs
import re
import sys

infile = codecs.open(sys.argv[1],'r','utf8').readlines()
outfile = codecs.open(sys.argv[1]+'.SHiST','w','utf8')

for line in infile:
	word,tag=line.strip().split()
	if line=='\n':
		outfile.write(line)
		

	elif tag[:3]=='ADJ':
		outfile.write(word+'\t'+'ADJ\n')
	elif tag[:3] =='APP':
		outfile.write(word+'\t'+'APP\n')
	elif tag =='ADV':
		outfile.write(word+'\t'+'AV\n')
	elif tag =='PWAV' or tag =='ADV':
		outfile.write(word+'\t'+'AV\n')
	elif tag[:3] =='PTK':
		outfile.write(word+'\t'+'PTK\n')
	elif tag in ['ART','PDAT','PDS']:
		if tag =='ART' and word.lower()[0]!='d':
			outfile.write(word+'\t'+'DI\n')
		else:	
			outfile.write(word+'\t'+'DD\n')
	elif tag in ['DRELS','PRELAT','PRELS']:
		outfile.write(word+'\t'+'DRELS\n')
	elif tag in ['PPOSAT','PPOSS']:
		outfile.write(word+'\t'+'DPOS\n')
	elif tag == 'PIAT':
		outfile.write(word+'\t'+'DI\n')
	elif tag =='PIS':
		outfile.write(word+'\t'+'PR\n')
	elif tag in ['PWAT','PWS']:
		outfile.write(word+'\t'+'DG\n')
	elif tag in ['PPER','PRF']:
		outfile.write(word+'\t'+'PR\n')
	elif tag in ['KON','KOUS','KOKOM','KOUI']:
		outfile.write(word+'\t'+'KO\n')
	elif tag =='NN':
		outfile.write(word+'\t'+'NA\n')
	elif tag in ['PAV','PWAV']:
		outfile.write(word+'\t'+'PAV\n')
	elif tag[:2]=='VV':
		outfile.write(word+'\t'+'VV\n')
	elif tag[:2]=='VA':
		outfile.write(word+'\t'+'VA\n')
	elif tag[:2]=='VM':
		outfile.write(word+'\t'+'VM\n')
	elif tag[0]=='$':
		outfile.write(word+'\t'+'$\n')
	elif tag =='TRUNC' or tag =='APZR':
		outfile.write(word+'\t'+'PTK\n')
	else:
		if tag not in ['NE','CARD','ITJ','FM']:
			print word 
			print tag
		outfile.write(word+'\t'+tag+'\n')

