import sys
import codecs

 

accuracy=[0.0] * 10

setnr=10

for i in range(setnr):
	found=0.0
	gold =codecs.open('set'+str(i)+'/'+sys.argv[1],'r','utf8').readlines()
	prediction = codecs.open('set'+str(i)+'/'+sys.argv[2],'r','utf8').readlines() 
	for nr,line in enumerate(gold):
		print line
		sg = line.split('\t')
		sp = prediction[nr].split('\t')


		if sg[1].strip()==sp[1].strip():
			found +=1

		else:
			print line
			print prediction[nr]
	

	accuracy[i]=float(found)/float(len(gold))	
print 'Average accuracy is :'+str(sum(accuracy)/10)
print 'The single accuracies are :'
for el in accuracy:
	print str(el)	
