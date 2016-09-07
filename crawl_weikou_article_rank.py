#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests,json,string
import codecs
from bs4 import BeautifulSoup 
from weikou_article import WeikouArticle
import time
import os
import random
from project.http.requests.proxy.requestProxy import RequestProxy

req_proxy = RequestProxy()

def read_books():
    with open("weikou_article.json","r") as account: 
        content = account.readlines()
        for line_number,line in enumerate(content):
        	print(json.loads(line))

def getMoreGzhAncCategoryInfo(weikou_article_obj):
	url = weikou_article_obj.author_link
	resp = req_proxy.generate_proxied_request(url)
	if response == None or not response.status_code == 200:
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
	resp = req_proxy.generate_proxied_request(url)
	if response == None or not response.status_code == 200:
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
		imageDivArray = article_page_div.findAll(lambda tag: tag.name == 'img' and 'data-echo' in tag.attrs)
		if len(imageDivArray) > 0:
			image_url = imageDivArray[0]["data-echo"].split("url=")[1].split('?')[0]
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
			if p.find(lambda tag: tag.name == 'img' and 'data-echo' in tag.attrs):
				# print("found img!")
				media_type = p.find('img')["data-echo"].split("wx_fmt=")[1]
				media_src = p.find('img')["data-echo"].split("url=")[1].split('?')[0]
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

	outPutFileName = "GHZArticle/article_weikou_rank_"+time.strftime("%Y%m%d")+".json"
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
	time.sleep(4)

def crawl_weikou(numPage):
	articles = []
	hrefs = []

	id_list = [(104,numPage),(109,numPage),(107,numPage),(127,numPage),(106,numPage),(103,numPage),(123,numPage),(102,numPage),(111,numPage),(110,numPage),(120,numPage),(108,numPage),(128,numPage),(121,numPage),(105,numPage),(119,numPage),(114,numPage),(101,numPage)]
	#id_list = [(127,numPage),(106,numPage),(103,numPage),(123,numPage),(102,numPage),(111,numPage),(110,numPage),(120,numPage),(108,numPage),(128,numPage),(121,numPage),(105,numPage),(119,numPage),(114,numPage),(101,numPage)]
	articleSet = set()
	with open("TrackingData/articleWeikouSet.txt",'r') as f:
		for line in f:
			articleSet.add(line.strip())

	random.shuffle(id_list)
	orgianalUrl = "http://www.vccoo.com/cateboard/?id=%s&page=%s"
	for (aid, page) in id_list:
		for pid in range(0, page):
			print("Procesing category : ", str(aid), " page : ", str(pid))
			url = orgianalUrl % (str(aid),str(pid))
			#response = requests.get(url,timeout=15)
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
			time.sleep(2)

		        
	        
                            

if __name__ == "__main__":
	
	crawl_weikou(25)
	#read_books()
	# start = time.time()
	# req_proxy = RequestProxy()
	# print "Initialisation took: ", (time.time()-start)
	# print "Size : ", len(req_proxy.get_proxy_list())
	# print " ALL = ", req_proxy.get_proxy_list()
    #
    #
	# while 1:
	# 	print "here"
	# 	start = time.time()
	# 	urlUrl = 'http://google.com'
	# 	request = req_proxy.generate_proxied_request(urlUrl)
	# 	print "Proxied Request Took: ", (time.time()-start), " => Status: ", request.__str__()
	# 	print "Proxy List Size: ", len(req_proxy.get_proxy_list())
    #
	# 	print"-> Going to sleep.."
	# 	time.sleep(2)


