#!/usr/bin/env python

# -*- coding: utf-8 -*-
import sys
import codecs
import os
import subprocess
import re
import sys
import json


setnr=10

for i in range(setnr):

	print i

	outf=codecs.open('set'+str(i)+'/tritrain','w','utf8')
	cat=subprocess.Popen(['cat','labeled_unlabeled', 'set'+str(i)+'/train'],stdout=outf)
	outf.close() 
	cat.communicate()
	train_f= 'set'+str(i)+'/tritrain'
	dev_f= 'set'+str(i)+'/dev'
	outfile= 'set'+str(i)+'/nn_tagged_tritrain'

	nn = subprocess.Popen(['python','POS_tag_SHiST.py','lrec.ini',train_f,dev_f,outfile])
	nn.communicate()
	index_dict = json.load(open('set'+str(i)+'/indices.json'))
	tagged_f = codecs.open('set'+str(i)+'/nn_tagged_tritrain','r','utf8')
	tagged_l= tagged_f.readlines()
	test_nn = codecs.open('set'+str(i)+'/test.tritraining','w','utf8')
	for el in index_dict['test']:		
		tokens = tagged_l[el].strip().split()
		for tok in tokens:
			t,l = tok.split('_')
			test_nn.write(t+'\t'+l+'\n')

	test_nn.close()
