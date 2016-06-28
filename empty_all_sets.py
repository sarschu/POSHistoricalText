import sys
import shutil
import os



setnr=10

for i in range(setnr):

	folder_path = './set'+str(i)
	for file_object in os.listdir(folder_path):
   		file_object_path = os.path.join(folder_path, file_object)
    		if os.path.isfile(file_object_path):
       			os.unlink(file_object_path)
    		else:
       			shutil.rmtree(file_object_path)
	#shutil.rmtree('./set'+str(i)+'/*')
	os.mkdir('./set'+str(i)+'/nn_training')
