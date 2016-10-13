#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests,json,string
import codecs
from bs4 import BeautifulSoup 
from weikou_article import WeikouArticle

def crawl_weikou_account():
	hrefs = []
	url_template = "http://www.vccoo.com/search?qa={account}"
	with open("TrackingData/gzhWeikouFamousAccount.txt","r") as accounts: 
		content = accounts.readlines()
		for line_number,account in enumerate(content):
			print(account.strip())
			accountlineArray = account.strip().split(",")
			url = url_template.format(account = accountlineArray[0])
			print(url)
			response = requests.get(url)
			soup = BeautifulSoup(response.text)
			divs = soup.findAll("div", {"class":"classify-list-con"})
			for div in divs:
				hrefs.append(div.find('a')['href'].encode()+","+str(accountlineArray[1])+","+str(accountlineArray[2]))

	for h in hrefs:
		print(h)
		with open("TrackingData/famousAccount.txt", 'a') as ff:
			ff.write(h+"\n")

if __name__ == "__main__":
	crawl_weikou_account()


