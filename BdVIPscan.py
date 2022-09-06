#!/usr/bin/env python
# -*- coding:utf-8 -*-

import grequests
import argparse
from re import search
from bs4 import BeautifulSoup
import urllib3
from tqdm import tqdm
from os import system, _exit
import platform
from time import sleep

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--min" ,help = "start location", metavar = "2000", required = True)
ap.add_argument("-e", "--max" ,help = "end location", metavar = "2200", required = True)
good = []

def clear():
	if(platform.system() == "Windows"):
		system("cls")
	else:
		system("clear")

def psrHTML(url,html):
	soup = BeautifulSoup(html,"html.parser")
	title = str(soup.title)
	re = search("百度网盘 ",title)
	if re:
		good.append(url)

def Scan(min,max):
	rs = []
	for i in range(min,max + 1):
		target = "https://pan.baidu.com/component/view/%s"%(i)
		try:
			rs.append(grequests.get(target, timeout = 3, verify = False)) #扫描
		except:
			pass
		finally:
			pbar.update(1)
			sleep(0.1)
	for i in grequests.map(rs):
		if i != None and i.status_code == 200:
			psrHTML(i.url, i.content)

if __name__=="__main__":
	args = ap.parse_args()
	min = int(args.min)
	max = int(args.max)
	if min > max or min / 1000 < 1 or max / 1000 < 1:
		print("参数错误！")
		_exit(0)
	print("开始进行扫描：")
	pbar = tqdm(total = max-min)
	Scan(min,max)
	pbar.close()
	# clear()
	print("扫描结束！")
	print("输出扫描结果：")
	with open("result.txt","w+",encoding='utf8') as f:
		f.write(args.min + " - " + args.max + "\n")
		print(args.min + " - " + args.max)
		for i in good:
			print(i)
			f.write(i + "\n")
	print("已保存到result.txt文件中，按回车键退出程序！")
	input()
	_exit(0)
