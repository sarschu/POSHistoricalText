import sys
import codecs
import random



setnr=10

for i in range(setnr):
	test_f= codecs.open('set'+str(i)+'/test','r','utf8').readlines()
	dev_f= codecs.open('set'+str(i)+'/dev','r','utf8').readlines()
	test_mhd= codecs.open('set'+str(i)+'/test_mhd','w','utf8')
	gold = codecs.open('set'+str(i)+'/test_gold','w','utf8')
	dev_gold=codecs.open('set'+str(i)+'/dev_gold','w','utf8')
	dev_mhd= codecs.open('set'+str(i)+'/dev_mhd','w','utf8')
	for line in test_f:
		tokens=line.strip().split()
		for tok in tokens:
			t,l = tok.split('_')
			test_mhd.write(t+'\n')
			gold.write(t+'\t'+l+'\n')
		test_mhd.write('\n')

	for line in dev_f:
		tokens=line.strip().split()
		for tok in tokens:
			t,l = tok.split('_')
			dev_mhd.write(t+'\n')
			dev_gold.write(t+'\t'+l+'\n')
		dev_mhd.write('\n')

			
	
	test_mhd.close()
	gold.close()
	dev_gold.close()
	dev_mhd.close()


	
