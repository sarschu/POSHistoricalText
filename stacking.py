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
	dev_mhd = codecs.open('set'+str(i)+'/dev.mhd','r','utf8').readlines()
	dev_nhd = codecs.open('set'+str(i)+'/dev.nhd','r','utf8').readlines()
	dev_nn = codecs.open('set'+str(i)+'/dev.nn','r','utf8').readlines()
	dev_crf = codecs.open('set'+str(i)+'/dev.crf','r','utf8').readlines()
	dev_gold = codecs.open('set'+str(i)+'/dev_gold','r','utf8').readlines()
	test_mhd = codecs.open('set'+str(i)+'/test.mhd','r','utf8').readlines()
	test_nhd = codecs.open('set'+str(i)+'/test.nhd','r','utf8').readlines()
	test_nn = codecs.open('set'+str(i)+'/test.nn','r','utf8').readlines()
	test_crf = codecs.open('set'+str(i)+'/test.crf','r','utf8').readlines()
	stack_train = codecs.open('set'+str(i)+'/train_stack','w','utf8')
	stack_test = codecs.open('set'+str(i)+'/test_stack','w','utf8')
	for tnr,line in enumerate(dev_mhd):
		t,l_mhd = line.strip().split('\t')
		t,l_nhd = dev_nhd[tnr].strip().split('\t')
		t,l_nn = dev_nn[tnr].strip().split('\t')
		t,l_crf = dev_crf[tnr].strip().split('\t')
		t,l_gold = dev_gold[tnr].strip().split('\t')		
		stack_train.write(t+'\t'+l_nn+'\t'+l_crf+'\t'+l_mhd+'\t'+l_nhd+'\t'+l_gold+'\n')
		if t in ['.',':','!','?']:
			stack_train.write('\n')
	for tnr,line in enumerate(test_mhd):
		t,l_mhd = line.strip().split('\t')
		t,l_nhd = test_nhd[tnr].strip().split('\t')
		t,l_nn = test_nn[tnr].strip().split('\t')
		t,l_crf = test_crf[tnr].strip().split('\t')
		stack_test.write(t+'\t'+l_nn+'\t'+l_crf+'\t'+l_mhd+'\t'+l_nhd+'\n')
		if t in ['.',':','!','?']:
			stack_test.write('\n')
	stack_train.close()
	stack_test.close()
	stack_test = 'set'+str(i)+'/test_stack'
	stack_train = 'set'+str(i)+'/train_stack'
	model = 'set'+str(i)+'/stacking.model'
	stacking_out = codecs.open('set'+str(i)+'/test.stacking_tmp','w','utf8')
	# train the CRF
	crf_learn = subprocess.Popen(['/mount/arbeitsdaten13/users/schulzsh/tools/CRF++-0.58/crf_learn','template_stacking',stack_train,model])
	crf_learn.communicate()
	#test CRF
	crf_test = subprocess.Popen(['/mount/arbeitsdaten13/users/schulzsh/tools/CRF++-0.58/crf_test','-m',model,stack_test],stdout=stacking_out)
	stacking_out.close()
	crf_test.communicate()
	tagged =codecs.open('set'+str(i)+'/test.stacking_tmp','r','utf8').readlines()
	out =codecs.open('set'+str(i)+'/test.stacking','w','utf8')
	for line in tagged:
		s_l= line.split()
		if len(s_l) >2:
			out.write(s_l[0]+'\t'+s_l[-1]+'\n')
	os.remove('set'+str(i)+'/test.stacking_tmp')
	
	
