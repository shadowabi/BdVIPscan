#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author:Sh4d0w_小白

from requests import get
from sys import argv
from queue import Queue
from threading import Thread
from time import sleep
from re import match
from bs4 import BeautifulSoup

q = Queue()

def Usage():
    print("[Usage]python BdVIPscan.py [min(recommend >= 100)] [max(recommend <= 999)]")

def psrHTML(url,html):
	soup = BeautifulSoup(html,'lxml')
	title = str(soup.find("title")).replace("<title>","")
	re = match(title, "百度网盘 \|")
	if(re != None):
		return url

def Scan():
	if(q.empty() == False):
		number = q.get()
		url = "https://pan.baidu.com/component/view/%s4"%(number)
		try:
			r = get(url)
			good = psrHTML(url, r.content)
			print("[+] " + good)
		except:
			pass
		finally:
			q.task_done()


def intoQueue(min ,max):
	for i in range(int(min) ,int(max) + 1):
		q.put(i)

if __name__=="__main__":
	try:
		min = argv[1]
		max = argv[2]
		if(min > max):
			raise	
		intoQueue(min,max)
		print("开始进行扫描：")
		for i in range(20):
			t = Thread(target = Scan)
			sleep(0.1)
			t.start()
			#t.join(1)
		print("扫描结束！")
	except:
		Usage()