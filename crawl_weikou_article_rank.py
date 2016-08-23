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



def crawl_weikou():
	articles = []
	hrefs = []
	#id_list = [(104,32),(109,32),(107,32),(127,32),(106,32),(103,32),(123,32),(102,32),(111,32),(110,32),(120,32),(108,32),(128,32),(121,32),(105,32),(119,32),(114,32),(101,32)]
	id_list = [(107,10)]

	orgianalUrl = "http://www.vccoo.com/cateboard/?id=%s&page=%s"
	for (aid, page) in id_list:
		for pid in range(0, page):
			print("Procesing category : ", str(aid), " page : ", str(pid))
			url = orgianalUrl % (str(aid),str(pid))
			response = requests.get(url)
			soup = BeautifulSoup(response.text)
			divs = soup.findAll("div", {"class":"classify-list-con"})
			for div in divs:
				hrefs.append(div.find('a')['href'])
	print("start getting articles")

	articles = []
	for h in hrefs:
		print(h)
		weikou_article_obj = WeikouArticle()
		resp = requests.get(h)
		page_soup = BeautifulSoup(resp.text)
		article_page_div = page_soup.find("div", {"class":"article-container"})

		title = article_page_div.find('h1').text.strip()
		author_div = article_page_div.find("div", {"class":"author-name"})
		author_link = author_div.find('a')['href']
		author_name = author_div.find('a').text.strip()
		image_url = ""

		try:
			image_url = article_page_div.find('img',{"data-type" : "jpeg"})["data-echo"].split("url=")[1].split('?')[0]
		except Exception,e:
			print("image grabing error:"+h)
			continue

		weikou_article_obj.title = title
		weikou_article_obj.author_link = author_link
		weikou_article_obj.author_name = author_name
		weikou_article_obj.image_url = image_url

		print(title)
		article_content = article_page_div.find("div",{"class" : "article-content"})
		content = ""

		image_tag = """<media>{"type":"%s","url","%s"}</media>"""

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
					# print("no img found")
		except:
			print("image parsing error:"+h)
			continue
		
		weikou_article_obj.content = content

		print(weikou_article_obj.to_JSON())
		b = weikou_article_obj.to_JSON()
		articles.append(b)

	outPutFileName = "GHZArticle/weikou_ranking_article"+time.strftime("%Y%m%d")+".json"
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

		        
	        
                            

if __name__ == "__main__":
	
	crawl_weikou()
	#read_books()


