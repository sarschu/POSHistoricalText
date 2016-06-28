import sys
import codecs
import random
import subprocess
import json



setnr=10

for i in range(setnr):
	train_f= 'set'+str(i)+'/train'
	dev_f= 'set'+str(i)+'/dev'
	outfile= 'set'+str(i)+'/nn_tagged_self'

	nn = subprocess.Popen(['python','POS_tag_self2.py','lrec.ini',train_f,dev_f,outfile,'set'+str(i)+'/indices.json'])
	nn.communicate()
	
	index_dict = json.load(open('set'+str(i)+'/indices.json'))
	tagged_f = codecs.open('set'+str(i)+'/nn_tagged_self','r','utf8')
	tagged_l= tagged_f.readlines()
	test_nn = codecs.open('set'+str(i)+'/test.nn_self','w','utf8')
	for el in index_dict['test']:		
		tokens = tagged_l[el].strip().split()
		for tok in tokens:
			t,l = tok.split('_')
			test_nn.write(t+'\t'+l+'\n')

	test_nn.close()
