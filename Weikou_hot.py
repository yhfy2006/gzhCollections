#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests,json
import codecs
from bs4 import BeautifulSoup 
from gzhPojo import WeixinAccount
import time
import os

def crawl_weixin():

    ghzSet = set()
    with open("TrackingData/gzhWeikouAccoutSet.txt",'r') as f:
        for line in f:
            ghzSet.add(line.strip())


    accounts = []
    hrefs = []
    response = requests.get("http://www.vccoo.com/leaderboard")
    soup = BeautifulSoup(response.text)
    divs = soup.findAll("div", {"class":"normal-con"})

    for div in divs:
        hrefs.append(div.find('a')['href'])


    outPutFileName = "GZHData/gzh_Weikou_hot_"+time.strftime("%Y%m%d")+".csv"

    if not os.path.exists(os.path.dirname(outPutFileName)):
        try:
            os.makedirs(os.path.dirname(outPutFileName))
        except OSError as exc: # Guard against race condition
            if exc.errno != exc.EEXIST:
             raise

    with codecs.open(outPutFileName,"a","utf-8") as weixin_file:
        for href in hrefs:
            weixin_account_obj = WeixinAccount()
            resp = requests.get(href)
            page_soup = BeautifulSoup(resp.text)

            category_div = page_soup.find("div", {"class":"crumbs"})
            category = category_div.findAll('a')[1].text

            account = page_soup.find("div", {"class":"row publicAccountInfo"})
            account_name = account.find('h3').text
            account_id = account.find("span",{"class":"publicAccountID"}).text
            account_total_articles = account.find("span",{"class":"totalNumberOfArticles"}).text.split(u"：")[-1]
            account_last_week_read = account.find("span",{"class":"lastWeekRead"}).text.split(u"：")[-1]
            account_record_date = account.find("span",{"class":"recordDate"}).text.split(u"：")[-1]

            weixin_account_obj.accountName = account_name
            weixin_account_obj.aid = account_id
            weixin_account_obj.url = href
            weixin_account_obj.total_articles = account_total_articles
            weixin_account_obj.last_week_read = account_last_week_read
            weixin_account_obj.last_modified_date = account_record_date
            weixin_account_obj.category = category
            weixin_account_obj.ctgTag = category

            if not account_id in ghzSet:
                resultStr = weixin_account_obj.accountName+","+weixin_account_obj.aid+","+weixin_account_obj.url.encode("utf-8")+","+weixin_account_obj.category+","+str(weixin_account_obj.total_articles)+","+str(weixin_account_obj.last_week_read)+","+weixin_account_obj.last_modified_date+","+weixin_account_obj.ctgTag+"\n"
                print(resultStr)
                weixin_file.write(resultStr)

                ghzSet.add(account_id)
                try:
                    with open("TrackingData/gzhWeikouAccoutSet.txt",'a') as ff:
                        ff.write(account_id+"\n")
                except Exception,e:
                    continue
            else:
                print(u"已存在---》"+weixin_account_obj.accountName)
                pass







if __name__ == "__main__":
    crawl_weixin()