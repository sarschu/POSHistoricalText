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
import json

setnr=10

for i in range(setnr):
	index_dict = json.load(open('set'+str(i)+'/indices.json'))
	tagged_f = codecs.open('set'+str(i)+'/nn_tagged_withoutRules','r','utf8')
	tagged_l= tagged_f.readlines()
	test_nn = codecs.open('set'+str(i)+'/test.nn','w','utf8')
	dev_nn = codecs.open('set'+str(i)+'/dev.nn','w','utf8')

	for el in index_dict['dev']:
		tokens = tagged_l[el].strip().split()
		for tok in tokens:
			t,l = tok.split('_')
			dev_nn.write(t+'\t'+l+'\n')
	
	for el in index_dict['test']:		
		tokens = tagged_l[el].strip().split()
		for tok in tokens:
			t,l = tok.split('_')
			test_nn.write(t+'\t'+l+'\n')

	test_nn.close()
	dev_nn.close()
