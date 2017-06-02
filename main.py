#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import requests
import threading
from lxml.html import fromstring

class cnBLogSpider:

	Threads = []
	requestHeader = {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, sdch",
		"Accept-Language":"en-US,en;q=0.8,zh;q=0.6,zh-TW;q=0.4",
		"Cache-Control":"no-cache",
		"Host":"www.cnblogs.com",
		"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	}

	def __init__(self,userName,startP,endP,threadSize = 50):
		self.queryCount(startP)
		self.queryCount(endP)
		self.queryCount(threadSize,2)
		if startP > endP:
			raise "startcount could not bigger than endcount!"
		self.userName = userName
		self.startP = int(startP)
		self.endP = int(endP)
		self.threadSize = int(threadSize)

	def queryCount(self,tempCount,countType = 1):
		try:
			if countType == 1:
				if int(tempCount) < 1000000 or int(tempCount) > 9999999:raise
			else:
				if int(tempCount) < 1:raise
		except:
			raise "Error Input!"

	def pageGen(self):
		while self.startP <= self.endP:
			yield self.startP
			self.startP += 1
		else:
			StopIteration

	def getTitle(self,htmlContents):
		tempTitle = fromstring(htmlContents.content)
		tempTitle = tempTitle.findtext('.//title')
		return tempTitle

	def queryLogFile(self):
		if os.path.exists('./resLog.log'):
			self.logFile = open("./resLog.log",'a')
		else:
			self.logFile = open("./resLog.log",'w')

	def getHtmlContents(self,Url):
		tempHtmlContents = requests.get(Url,headers=self.requestHeader)
		if tempHtmlContents.status_code == 200:
			tempRes = self.getTitle(tempHtmlContents)
			self.logFile.write("%s\t%s\n" %(tempRes,Url))
			self.logFile.flush()
			print("[%s] - got articles -> %s" %(Url,tempRes))

	def runThread(self):
		for tempThread in self.Threads:
			tempThread.start()
			while True:
				if len(threading.enumerate()) < self.threadSize:
					break

	def run(self):
		print("Spider Starting...")
		self.queryLogFile()
		print("Loding %s Urls..." %self.userName)
		for tempP in self.pageGen():
			tempUrl = "http://www.cnblogs.com/%s/articles/%s.html" %(self.userName,tempP)
			self.Threads.append(threading.Thread(target=self.getHtmlContents,args=(tempUrl,)))
		print("Url Loding done , starting Crawing...".center(50, '#'))
		self.runThread()

if __name__ == "__main__":
	if len(sys.argv) == 4 :
		cnbs = cnBLogSpider(sys.argv[1], sys.argv[2],sys.argv[3])
		cnbs.run()
	elif len(sys.argv) == 5:
		cnbs = cnBLogSpider(sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4])
		cnbs.run()
	else:
		print("python3 main.py { username } { start count } { end count } [threadcount]")

