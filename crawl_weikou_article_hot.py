#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests,json,string
import codecs
from bs4 import BeautifulSoup 
from weikou_article import WeikouArticle
import time
import os


def read_books():
    with open("weikou_article.json","r") as account: 
        content = account.readlines()
        for line_number,line in enumerate(content):
        	print(json.loads(line))

def getMoreGzhAncCategoryInfo(weikou_article_obj):
	url = weikou_article_obj.author_link
	resp = requests.get(url)
	if not resp.status_code == 200:
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
	weikou_article_obj = WeikouArticle()
	resp = requests.get(url)
	if not resp.status_code == 200:
		return

	page_soup = BeautifulSoup(resp.text)
	article_page_div = page_soup.find("div", {"class":"article-container"})

	title = article_page_div.find('h1').text.strip()
	author_div = article_page_div.find("div", {"class":"author-name"})
	author_link = author_div.find('a')['href']
	author_name = author_div.find('a').text.strip()
	articleDate = author_div.text.strip().split(' ')[1]
	image_url = ""

	try:
		image_url = article_page_div.find('img',{"data-type" : "jpeg"})["data-echo"].split("url=")[1].split('?')[0]
	except Exception,e:
		print("image grabing error:"+url)
		return


	weikou_article_obj.title = title
	weikou_article_obj.author_link = author_link
	weikou_article_obj.gzh_name = author_name
	weikou_article_obj.image_url = image_url
	weikou_article_obj.articleDate = articleDate

	#paint with ctg
	try:
		getMoreGzhAncCategoryInfo(weikou_article_obj)
	except Exception,e:
		print("parsing gzh error:"+url)
		return

	print(title)
	article_content = article_page_div.find("div",{"class" : "article-content"})
	content = ""

	image_tag = """<media>{"type":"%s","url","%s"}</media>"""

	hasSetIntro = False
	try:
		for p in article_content.findAll('p'):
			if p.find('img'):
				# print("found img!")
				media_type = p.find('img')["data-type"]
				media_src = p.find('img',{"data-type" : media_type})["data-echo"].split("url=")[1].split('?')[0]
				media_line = image_tag % (media_type,media_src)
				print(media_line)
				content += '\n' + media_line
			else:
				content += '\n' + p.text
				if not hasSetIntro:
					weikou_article_obj.intro = p.text
					hasSetIntro = True
				# print("no img found")
	except:
		print("image parsing error:"+url)
		return

	weikou_article_obj.content = content

	print(weikou_article_obj.to_JSON())
	b = weikou_article_obj.to_JSON()

	outPutFileName = "GHZArticle/weikou_baowen_article"+time.strftime("%Y%m%d")+".json"
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
	#with open("articleWeikouSet.txt",'r') as f:
		#for line in f:
			#articleSet.add(line.strip())

	orgianalUrl = "http://www.vccoo.com/hotarticle/?page=%s"
	for pid in range(1,pageNumber):
		print("Procesing page " + str(pid))
		url = orgianalUrl % str(pid)
		response = requests.get(url,timeout=10)
		if not response.status_code == 200:
			continue
		soup = BeautifulSoup(response.text)
		divs = soup.findAll("div", {"class":"classify-list-con"})
		for div in divs:
			h = div.find('a')['href']
			if not h in articleSet:
				getArticleDetails(h)
				with open("articleWeikouSet.txt",'a') as ff:
					ff.write(h+"\n")
				articleSet.add(h)
			else:
				print("exsist-> "+h)




if __name__ == "__main__":
	
	crawl_weikou(100)
	#read_books()

