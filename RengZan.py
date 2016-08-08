# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
from gzhPojo import WeixinAccount
import re


class gzhRengZan:

    #print(sys.getdefaultencoding())
    webSiteUrl = "www.rengzan.com/"
    def crawlRengZan(self):

        r = requests.get("http://"+self.webSiteUrl)
        #print(r.text)
        soup = BeautifulSoup(r.text)
        div = soup.find("div",{"class":"introc"})
        h3 = soup.find("h3")
        h3Value = h3.getText()
        h3CtgMapped = self.ctgMapping(h3Value)
        for link in div.find_all("a",{"target":"_blank"}):
            str = link.get('href')
            finalUrl = self.webSiteUrl+str
            self.crawRengzanPage(finalUrl,h3CtgMapped)
            print(str)


    def crawRengzanPage(self,url,ctg):
        r = requests.get("http://" +url)
        soup = BeautifulSoup(r.text)
        div = soup.find("div",{"class":"resourcese"})
        divPage = div.find("div",{"class":"pagewx"})
        pageA = divPage.find_all("a")[-1]
        pageAStr = pageA.get('href').split("-")[-1]
        pageATotalNumber = pageAStr.replace(".html","")
        for page in range(1,int(pageATotalNumber)):
            print("page = " + str(page))
            urlTmp = url.replace(".html","")
            urlTmp = urlTmp+"-p-"+pageATotalNumber+".html"
            r1 = requests.get("http://" +urlTmp)
            soup1 = BeautifulSoup(r1.text)
            div1 = soup1.find("div",{"class":"resourcese"})
            for li in div1.find_all("li",{"class":"author-item-li"}):
                a = li.find("a")
                href = a.get("href")
                finalUrl = self.webSiteUrl+href
                self.crawRengzanGZHDetails(finalUrl,ctg)

    def crawRengzanGZHDetails(self,url,ctg):
        r = requests.get("http://" +url)
        soup = BeautifulSoup(r.text)
        div = soup.find("div",{"class":"cont"})
        resultsLis = div.find_all("li")
        weixinNameLiStr = resultsLis[0].getText().split('\n')[2].strip()
        weixinAccountLiStr = resultsLis[1].getText().split('\n')[2].strip()

        newGzhObj = WeixinAccount()
        newGzhObj.accountName = weixinNameLiStr
        newGzhObj.aid = weixinAccountLiStr
        newGzhObj.category = ctg
        newGzhObj.url = url

        print(newGzhObj.accountName)
        print(newGzhObj.aid)
        print(newGzhObj.category)
        print(newGzhObj.url)

        print("\n\n")


    def ctgMapping(self,ctg):
        output = ""
        if ctg == u"新闻": output="时事·城市"
        if ctg == u"名人": output="媒体·达人"
        if ctg == u"美食": output="健康·美食"
        if ctg == u"影娱": output="电影·音乐"
        if ctg == u"购物": output="时尚·格调"
        if ctg == u"家居": output="生活·情感"
        if ctg == u"天气": output="天气·气象"
        if ctg == u"旅游": output="休闲·旅行"
        if ctg == u"宠物": output="宠物·宠物"
        if ctg == u"社交": output="社交·交友"
        if ctg == u"体育": output="运动·赛事"
        if ctg == u"高校": output="教育·励志"
        if ctg == u"互联网": output="数码·科技"
        if ctg == u"医疗": output="健康·美食"
        if ctg == u"育儿": output="教育·励志"
        return output




a = gzhRengZan()
a.crawlRengZan()