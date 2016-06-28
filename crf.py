#!/usr/bin/env python

# -*- coding: utf-8 -*-
import sys
import codecs
import os
import subprocess
import re
import sys


setnr=10

for i in range(setnr):
	train = codecs.open('set'+str(i)+'/train','r','utf8').readlines()
	test = codecs.open('set'+str(i)+'/test','r','utf8').readlines()
	dev = codecs.open('set'+str(i)+'/dev','r','utf8').readlines()
	crf_trainformat = codecs.open('set'+str(i)+'/train_crf','w','utf8')
	crf_testformat = codecs.open('set'+str(i)+'/test_crf','w','utf8')
	crf_devformat = codecs.open('set'+str(i)+'/dev_crf','w','utf8')
	for tnr,line in enumerate(train):
		split_l=line.strip().split()
		for tok in split_l:
			t,l = tok.strip().split('_')		
			crf_trainformat.write(t+'\t'+l+'\n')
		crf_trainformat.write('\n')
	crf_trainformat.close()
	for tnr,line in enumerate(test):
		split_l=line.strip().split()
		for tok in split_l:
			t,l = tok.strip().split('_')		
			crf_testformat.write(t+'\n')
		crf_testformat.write('\n')	
	crf_testformat.close()
	for tnr,line in enumerate(dev):
		split_l=line.strip().split()
		for tok in split_l:
			t,l = tok.strip().split('_')		
			crf_devformat.write(t+'\n')
		crf_devformat.write('\n')	
	crf_devformat.close()


	crf_test = 'set'+str(i)+'/test_crf'
	crf_dev =  'set'+str(i)+'/dev_crf'
	crf_train = 'set'+str(i)+'/train_crf'
	model = 'set'+str(i)+'/crf.model'
	crf_tmp = codecs.open('set'+str(i)+'/test.crf_tmp','w','utf8')
	crf_out = codecs.open('set'+str(i)+'/test.crf','w','utf8')
	crf_dev_tmp = codecs.open('set'+str(i)+'/dev.crf_tmp','w','utf8')
	crf_dev_out = codecs.open('set'+str(i)+'/dev.crf','w','utf8')
	# train the CRF
	crf_learn = subprocess.Popen(['/mount/arbeitsdaten13/users/schulzsh/tools/CRF++-0.58/crf_learn','template_crf',crf_train,model])
	crf_learn.communicate()
	#test CRF
	crf_t = subprocess.Popen(['/mount/arbeitsdaten13/users/schulzsh/tools/CRF++-0.58/crf_test','-m',model,crf_test],stdout=crf_tmp)

	crf_t.communicate()
	crf_tmp.close()
	lines = codecs.open('set'+str(i)+'/test.crf_tmp','r','utf8').readlines()
	for line in lines:
		if line.strip()!='':
			crf_out.write(line)

	crf_out.close()

	crf_d = subprocess.Popen(['/mount/arbeitsdaten13/users/schulzsh/tools/CRF++-0.58/crf_test','-m',model,crf_dev],stdout=crf_dev_tmp)

	crf_d.communicate()
	crf_dev_tmp.close()
	lines = codecs.open('set'+str(i)+'/dev.crf_tmp','r','utf8').readlines()
	for line in lines:
		if line.strip()!='':
			crf_dev_out.write(line)

	crf_dev_out.close()
	
