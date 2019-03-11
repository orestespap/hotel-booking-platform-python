import pickle
import json
#https://www.geeksforgeeks.org/reading-writing-text-files-python/
#https://www.w3schools.com/python/python_file_open.asp

def grab_(filename):
	with open(filename,'rb') as afile:
		data=pickle.load(afile)
	return data

def save_(data,filename):
	with open(filename,'wb') as afile:
		pickle.dump(data,afile)


def jsonload_(filename):
	with open(filename,encoding='utf8') as afile:
		data=json.load(afile)
	return data

def jsonsave_(data,filename):
	with open(filename, 'w') as afile:
		json.dump(data, afile)

def create_text_file(filename):
	with open(filename,'w') as afile:
		pass

def read_file(filename,encoding='utf8'):
	with open(filename,'r') as afile:
		return afile.read()

def list_lines_txt(filename,encoding='utf8'):
	with open(filename,'r') as afile:
		return [aline for aline in afile]

def write_to_text_file(filename,f_string):
	with open(filename,'a') as afile:
		afile.write(f_string+'\n')

def write_to_text_file_args(filename,*f_strings):
	with open(filename,'a') as afile:
		for f_string in f_strings:
			afile.write(f_string+'\n')
