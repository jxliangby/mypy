import os
import glob
import time
from fnmatch import fnmatch

import csv
from collections import namedtuple

def fileread(path,logpath):
	with open(logpath, 'a') as log:
		print("open file path:%s" %(path),file=log)
		with open(path, 'rt') as f:
			for line in f:
				print(line,file=log)
			
def findfiles(path):
	pys = glob.glob(path+"*.py")
	name_sz_date = [(name,os.path.getsize(name),os.path.getmtime(name)) for name in pys]
	for name,size,mtime in name_sz_date:
		print(name,size, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(mtime)))
	
	pys2 = [name for name in os.listdir(path) if fnmatch(name, "*.py")]
	print(pys2)



def docsv(path):
	'''do read'''
	with open(path) as f:
		f_csv = csv.reader(f)
		headings = next(f_csv)
		Row = namedtuple('Row', headings)
		for r in f_csv:
			row = Row(*r)
			print("row data id:%s,name:%s,age:%s" %(row.id,row.name,row.age))

    
    
def witercsv(path):
	writer_rows = [(12,'Bob',44),
				   (13,'Joy',19)
				   ]
	with open(path, 'a+',newline='') as wf:
		f_csv = csv.writer(wf)
		f_csv.writerows(writer_rows)


rootPath = os.getcwd() + "\\"
logpath = rootPath + "log.txt"

#fileread(rootPath+"myfile.py",logpath)
#findfiles(rootPath)

csvPath = 'demo.csv'
witercsv(csvPath)
docsv(csvPath)