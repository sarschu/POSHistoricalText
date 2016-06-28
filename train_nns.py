import sys
import codecs
import random
import subprocess


setnr=10

for i in range(setnr):
	train_f= 'set'+str(i)+'/train'
	dev_f= 'set'+str(i)+'/dev'
	outfile= 'set'+str(i)+'/nn_tagged'

	nn = subprocess.Popen(['python','POS_tag_SHiST.py','lrec.ini',train_f,dev_f,outfile])
	nn.communicate()
	
