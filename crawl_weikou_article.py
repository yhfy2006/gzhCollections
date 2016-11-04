#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests,json,string
import codecs
from bs4 import BeautifulSoup
import time
import os
from weikou_article import WeikouArticle
from project.http.requests.proxy.requestProxy import RequestProxy
import random
from common import getWeikouArticleObj


req_proxy = RequestProxy()
req_proxy.useProxy = False

import sys

reload(sys)
sys.setdefaultencoding('utf8')
outPutFileName = "GZHLabeledData/weikou_labeled_article_"+time.strftime("%Y%m%d")+".json"

def read_books():
    with open("GZHLabeledData/weikou_article.json","r") as account:
        content = account.readlines()
        for line_number,line in enumerate(content):
        	print(json.loads(line))
         
def crawl_weikou_by_userpage(contentString):
	hrefsTuples = []
	contentStringS = contentString.strip().split(',')
	user_home_page = contentStringS[0]
	resp = req_proxy.generate_proxied_request(user_home_page)
	if resp == None or not resp.status_code == 200:
		return
	soup = BeautifulSoup(resp.text)
	pages = soup.find("div", {"class":"mainAuthor-page"})
	number_of_pages =  len(pages.findAll("li")) - 2
	for i in range(1, number_of_pages + 1):
		url = user_home_page + "?page=" + str(i)
		response = req_proxy.generate_proxied_request(url)
		if response == None or not resp.status_code == 200:
			continue
		soup = BeautifulSoup(response.text)
		divs = soup.findAll("div", {"class":"articlesItem"})
		for div in divs:
			hrefsTuples.append((div.find('a')['href'],contentStringS[1],contentStringS[2]))
	return hrefsTuples

def crawl_weikou_by_article_href(href):
	articles = []
	weikou_article_obj = getWeikouArticleObj(href[0],req_proxy)
	if weikou_article_obj is None:
		return
	
	if str(href[1]) is not None:
		weikou_article_obj.gzhCategory = str(href[1])
	if str(href[2]) is not None:
		weikou_article_obj.articleTopic = str(href[2])
	print(weikou_article_obj.to_JSON())
	b = weikou_article_obj.to_JSON()
	articles.append(b)


	if not os.path.exists(os.path.dirname(outPutFileName)):
		try:
			os.makedirs(os.path.dirname(outPutFileName))
		except OSError as exc: # Guard against race condition
			if exc.errno != exc.EEXIST:
			 raise
	with codecs.open(outPutFileName,"a","utf-8") as weikou_article_file:
		for article in articles:
		# 	weikou_article_file.write(article)
		    json.dump(article, weikou_article_file, ensure_ascii=False)
		    weikou_article_file.write('\n')

def crawl_weikou():
	articles = []
	hrefs = []
	id_list = [(104,1)]
	url = "http://www.vccoo.com/cateboard/?id={aid}&page={page}"
	for (aid, page) in id_list:
		for pid in range(0, page):
			print("Procesing category : ", str(aid), " page : ", str(page))
			url = url.format(aid = aid, page = pid)
			response = requests.get(url)
			soup = BeautifulSoup(response.text)
			divs = soup.findAll("div", {"class":"classify-list-con"})
			for div in divs:
				hrefs.append(div.find('a')['href'])
	print(hrefs)

	articles = []
	for h in hrefs:
		weikou_article_obj = WeikouArticle()
		resp = req_proxy.generate_proxied_request(href)
		if resp == None or not resp.status_code == 200:
			continue
		page_soup = BeautifulSoup(resp.text)
		article_page_div = page_soup.find("div", {"class":"article-container"})

		title = article_page_div.find('h1').text.strip()
		author_div = article_page_div.find("div", {"class":"author-name"})
		author_link = author_div.find('a')['href']
		author_name = author_div.find('a').text.strip()
		image_url = article_page_div.find('img',{"data-type" : "jpeg"})["data-echo"].split("url=")[1].split('?')[0]
		
		weikou_article_obj.title = title
		weikou_article_obj.author_link = author_link
		weikou_article_obj.author_name = author_name
		weikou_article_obj.image_url = image_url

		print(title)
		article_content = article_page_div.find("div",{"class" : "article-content"})
		content = ""

		image_tag = """<media>{"type":"%s","url","%s"}</media>"""

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
				# print("no img found")
		
		weikou_article_obj.content = content

		print(weikou_article_obj.to_JSON())
		b = weikou_article_obj.to_JSON()
		articles.append(b)

	with codecs.open("GZHLabeledData/weikou_article.json","a","utf-8") as weikou_article_file:
		for article in articles:
		# 	weikou_article_file.write(article)
		    json.dump(article, weikou_article_file, ensure_ascii=False)
		    weikou_article_file.write('\n')

		       
if __name__ == "__main__":
	
	#crawl_weikou_by_article_href("http://www.vccoo.com/v/990b8a")
	#crawl_weikou_by_article_href("http://www.vccoo.com/v/bdf6e8")
	articleSet = set()
	with open("TrackingData/articleLabeledWeikouSet.txt", 'r') as f:
		for line in f:
			articleSet.add(line.strip())

	with open("TrackingData/famousAccount.txt") as accounts:
		originalContent = accounts.readlines()
		content = random.sample(originalContent, len(originalContent))
		for user_home_page in content:
			hrefs = crawl_weikou_by_userpage(user_home_page)
			if hrefs == None:
				continue
			for hrefTuple in hrefs:
				if not hrefTuple[0] in articleSet:
					crawl_weikou_by_article_href(hrefTuple)
					with open("TrackingData/articleLabeledWeikouSet.txt",'a') as ff:
						ff.write(hrefTuple[0]+"\n")
					articleSet.add(hrefTuple[0])
				else:
					print("exsist-> " + hrefTuple[0])
					pass

	#crawl_weikou()
	#read_books()


