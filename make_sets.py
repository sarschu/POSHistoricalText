import sys
import codecs
import random
import json


all_sents=codecs.open(sys.argv[1],'r','utf8').readlines()

setnr=10
myList=[i for i in range(250)]

for i in range(setnr):
	index_dict={'train':[],'test':[],'dev':[]}
	test_f= codecs.open('set'+str(i)+'/test','w','utf8')
	dev_f= codecs.open('set'+str(i)+'/dev','w','utf8')
	train_f= codecs.open('set'+str(i)+'/train','w','utf8')
	random.shuffle(myList)
	for lnr in myList[:100]:
		index_dict['train']=myList[:100]
		train_f.write(all_sents[lnr])	
	for lnr in myList[100:200]:
		index_dict['dev']=myList[100:200]
		dev_f.write(all_sents[lnr])	
	for lnr in myList[200:]:
		index_dict['test']=myList[200:]
		test_f.write(all_sents[lnr])
	jsfile = open('set'+str(i)+'/indices.json', 'w')
	json.dump(index_dict,jsfile)
	jsfile.close()
	test_f.close()
	train_f.close()
	dev_f.close()

	
