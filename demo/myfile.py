import os
import glob
from fnmatch import fnmatch

def fileread(path,logpath):
	with open(logpath, 'wt') as log:
		print("open file path:%s" %(path),file=log)
		with open(path, 'rt') as f:
			for line in f:
				print(line,file=log)
			
def findfiles(path):
	pys = glob.glob(path+"*.py")
	print(pys)
	
	pys2 = [name for name in os.listdir(path) if fnmatch(name, "*.py")]
	print(pys2)
				
rootPath = "d:\\workspace\\python\\mypy\\demo\\"
logpath = rootPath + "log.txt"

#fileread(rootPath+"01.py",logpath)
findfiles(rootPath)
	