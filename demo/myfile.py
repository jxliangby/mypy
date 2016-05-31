import os
import glob
import time
from fnmatch import fnmatch

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
				
rootPath = "d:\\workspace\\python\\mypy\\demo\\"
logpath = rootPath + "log.txt"

fileread(rootPath+"myfile.py",logpath)
#findfiles(rootPath)
	