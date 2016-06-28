import sys
import codecs
import random
import subprocess
import shutil


setnr=10

for i in range(setnr):
	test_f= codecs.open('set'+str(i)+'/test_mhd','r','utf8')
	dev_f=codecs.open('set'+str(i)+'/dev_mhd','r','utf8')
	test_mhd = codecs.open('set'+str(i)+'/test.mhd','w','utf8')
	test_nhd = codecs.open('set'+str(i)+'/test.nhd','w','utf8')
	dev_mhd = codecs.open('set'+str(i)+'/dev.mhd','w','utf8')
	dev_nhd = codecs.open('set'+str(i)+'/dev.nhd','w','utf8')

	mhd1 = subprocess.Popen(['/mount/arbeitsdaten13/users/schulzsh/tools/tree_tagger/cmd/tree-tagger-mhg'],stdin=test_f,stdout=test_mhd)
	mhd1.communicate()
	test_f.close()
	mhd2 = subprocess.Popen(['/mount/arbeitsdaten13/users/schulzsh/tools/tree_tagger/cmd/tree-tagger-mhg'],stdin=dev_f,stdout=dev_mhd)
	mhd2.communicate()
	test_f.close()
	dev_f.close
	dev_f=codecs.open('set'+str(i)+'/dev_mhd','r','utf8')
	test_f= codecs.open('set'+str(i)+'/test_mhd','r','utf8')

	nhd1 = subprocess.Popen(['/mount/arbeitsdaten13/users/schulzsh/tools/tree_tagger/cmd/tree-tagger-german'],stdin=test_f,stdout=test_nhd)
	nhd1.communicate()
	test_f.close()
	nhd2 = subprocess.Popen(['/mount/arbeitsdaten13/users/schulzsh/tools/tree_tagger/cmd/tree-tagger-german'],stdin=dev_f,stdout=dev_nhd)
	nhd2.communicate()
	dev_f.close()
	test_mhd.close()
	test_nhd.close()
	#test_n= codecs.open('set'+str(i)+'/test.nhd','r','utf8')
	m=subprocess.Popen(['python','map_STTS2SHIST.py','set'+str(i)+'/test.nhd'])
	m.communicate()	
	m2=subprocess.Popen(['python','map_STTS2SHIST.py','set'+str(i)+'/dev.nhd'])
	m2.communicate()
	shutil.move('set'+str(i)+'/test.nhd.SHiST','set'+str(i)+'/test.nhd')
	shutil.move('set'+str(i)+'/dev.nhd.SHiST','set'+str(i)+'/dev.nhd')
