import os
import glob
import time
from fnmatch import fnmatch

import csv
from collections import namedtuple

import json

from urllib.request import urlopen

from xml.etree.ElementTree import parse
from xml.etree.ElementTree import iterparse
from xml.etree.ElementTree import Element

from xml.etree.ElementTree import tostring


from collections import Counter

from datetime import datetime

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

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.list = ['a', 'b','c']
classes = {
	'Point' : Point
}

'''

'''
def obj2json(obj):
	d = {'__classname__' : type(obj).__name__}
	d.update(vars(obj))
	return d

'''

'''
def josn2obj(d):
	classname = d.pop('__classname__', None)
	if classname:
		cls = classes[classname]
		obj = cls.__new__(cls)
		for key,value in d.items():
			setattr(obj, key, value)
		return obj
	else:
		return d


def dojson():
	data = {
		'name':'Rocky',
		'shares':1000,
		'price':543.21
	}
	jsonStr = json.dumps(data)
	print('json to str : %s' %(jsonStr))

	jsondata = json.loads(jsonStr)
	print('name:%s' %(jsondata['name']))


	p = Point(3,4)
	s = json.dumps(p,default=obj2json)
	print("obj to json:%s" %(s))
	pp = json.loads(s, object_hook=josn2obj)
	print("json to obj x:%s,y:%s" %(pp.x,pp.y))



def doxml():
	try:
		u = urlopen('http://planetpython.org/rss20.xml')
		doc = parse(u)
		for item in doc.iterfind('channel/item'):
			title = item.findtext('title')
			date = item.findtext('pubDate')
			link = item.findtext('link')
			print('title:%s\ndate:%s\nlink:%s' %(title,date,link))
	except BaseException as e:
		print("error:\n%s" %(e))		

def parse_and_remove(filename, path):
	path_parts = path.split('/')
	doc = iterparse(filename,('start', 'end'))
	next(doc)
	tag_stack = []
	elem_stack = []
	for event, elem in doc:
		if event == 'start':
			tag_stack.append(elem.tag)
			elem_stack.append(elem)
		elif event == 'end':
			if tag_stack == path_parts:
				yield elem
				elem_stack[-2].remove(elem)
			try:
				tag_stack.pop()
				elem_stack.pop()
			except Exception as e:
				pass	
def parseXML():
	titleCounter = Counter()
	starttime = datetime.now()
	print("start time :%s" %(starttime))

	doc = parse('list.xml')
	for pothole in doc.iterfind('channel/item'):
		titleCounter[pothole.findtext('title')] += 1
	for title, num in titleCounter.most_common():
		print(title, num)

	endtime = datetime.now()
	print("endtime :%s" %(endtime))
	print("*" * 80)
	print("total time:%s" %((endtime - starttime).microseconds))
	
	print("*" * 80)
	'''
	####################################################
	'''
	titleCounter2 = Counter()
	starttime = datetime.now()
	print("start time :%s" %(starttime))
	data = parse_and_remove("list.xml","channel/item")
	for pothole in data:
		titleCounter2[pothole.findtext('title')] += 1
	for title, num in titleCounter2.most_common():
		print(title, num)
	endtime = datetime.now()
	print("endtime :%s" %(endtime))
	print("*" * 80)
	print("total time:%s" %((endtime - starttime).microseconds))
	print("*" * 80)

def dict2xml(tag, d):
	elem = Element(tag)
	for key, val in d.items():
		child = Element(key)
		child.text = str(val)
		elem.append(child)
	return elem
rootPath = os.getcwd() + "\\"
logpath = rootPath + "log.txt"

#fileread(rootPath+"myfile.py",logpath)
#findfiles(rootPath)

csvPath = 'demo.csv'
#witercsv(csvPath)
#docsv(csvPath)

#dojson()

#parseXML()

s = {'name':'rocky','xx':12,'account':{'id':111,'money':1000.88,'orders':[{'id':1,'trans_amt':100}, {'id':2,'trans_amt':200}]}}
e = dict2xml('aa', s)
print(tostring(e))