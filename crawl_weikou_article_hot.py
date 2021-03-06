#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests,json,string
import codecs
from bs4 import BeautifulSoup 
from weikou_article import WeikouArticle
import time
import os
from project.http.requests.proxy.requestProxy import RequestProxy
from common import getWeikouArticleObj

req_proxy = RequestProxy()


def read_books():
    with open("weikou_article.json","r") as account: 
        content = account.readlines()
        for line_number,line in enumerate(content):
        	print(json.loads(line))

def getMoreGzhAncCategoryInfo(weikou_article_obj):
	url = weikou_article_obj.author_link
	resp = req_proxy.generate_proxied_request(url)
	if resp == None or not resp.status_code == 200:
		return
	page_soup = BeautifulSoup(resp.text)
	ctgDiv = page_soup.find("div",{"class":"crumbs"})
	ctgA = ctgDiv.findAll('a')
	ctgText = ctgA[1].text.strip()
	weikou_article_obj.gzhCategory = ctgText
	gzhAccount = page_soup.find("span",{"class":"publicAccountID"}).text.strip()
	weikou_article_obj.gzh_account = gzhAccount

def getArticleDetails(url):
	print(url)
	weikou_article_obj = getWeikouArticleObj(url,req_proxy)

	print(weikou_article_obj.to_JSON())
	b = weikou_article_obj.to_JSON()

	outPutFileName = "GHZArticle/article_weikou_baowen_"+time.strftime("%Y%m%d")+".json"
	if not os.path.exists(os.path.dirname(outPutFileName)):
		try:
			os.makedirs(os.path.dirname(outPutFileName))
		except OSError as exc: # Guard against race condition
			if exc.errno != exc.EEXIST:
			 raise
	with codecs.open(outPutFileName,"a","utf-8") as weikou_article_file:
		# 	weikou_article_file.write(article)
		json.dump(b, weikou_article_file, ensure_ascii=False)
		weikou_article_file.write('\n')

def crawl_weikou(pageNumber):

	articleSet = set()
	with open("TrackingData/articleWeikouSet.txt",'r') as f:
		for line in f:
			articleSet.add(line.strip())

	orgianalUrl = "http://www.vccoo.com/hotarticle/?page=%s"
	for pid in range(1,pageNumber):
		print("Procesing page " + str(pid))
		url = orgianalUrl % str(pid)
		response = req_proxy.generate_proxied_request(url)
		if response == None or not response.status_code == 200:
			continue
		soup = BeautifulSoup(response.text)
		divs = soup.findAll("div", {"class":"classify-list-con"})
		for div in divs:
			h = div.find('a')['href']
			if not h in articleSet:
				getArticleDetails(h)
				with open("TrackingData/articleWeikouSet.txt",'a') as ff:
					ff.write(h+"\n")
				articleSet.add(h)
			else:
				print("exsist-> "+h)




if __name__ == "__main__":
	
	crawl_weikou(20)
	#read_books()


