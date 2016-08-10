# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
from gzhPojo import WeixinAccount
import re
import json


class gzhRengZan:

    ghzSet = set()
    finalResultList = list()
    gzhPageSet = set()
    totalNumber = 0
    with open("gzhAccoutSet.txt",'r') as f:
        for line in f:
            ghzSet.add(line.strip())

    with open("gzhPageSet.txt","r") as file:
        for line in file:
            gzhPageSet.add(line.strip())


    webSiteUrl = "www.rengzan.com/"
    def crawlRengZan(self):

        r = requests.get("http://"+self.webSiteUrl)
        soup = BeautifulSoup(r.text)
        div = soup.find("div",{"class":"introc"})
        for link in div.find_all("a",{"target":"_blank"}):
            try:
                str = link.get('href')
                finalUrl = self.webSiteUrl+str
                h3 = link.find("h3")
                h3Value = h3.getText()
                print(h3Value+"\n\n")
                h3CtgMapped = self.ctgMapping(h3Value)
                self.crawRengzanPage(finalUrl,h3CtgMapped)
                print(str)
            except Exception,e:
                print("First level exception" + str(e))
                continue
            #break
        # with open('results.json', 'w') as f:
        #     json.dump(self.finalResultList, f,ensure_ascii=False,encoding="utf-8")


    def crawRengzanPage(self,url,ctg):
        r = requests.get("http://" +url)
        soup = BeautifulSoup(r.text)
        div = soup.find("div",{"class":"resourcese"})
        divPage = div.find("div",{"class":"pagewx"})
        pageA = divPage.find_all("a")[-1]
        pageAStr = pageA.get('href').split("-")[-1]
        pageATotalNumber = pageAStr.replace(".html","")
        for page in range(1,int(pageATotalNumber)):
            try:
                print("page = " + str(page))
                urlTmp = url.replace(".html","")
                urlTmp = urlTmp+"-p-"+str(page)+".html"
                pageUrl = "http://" +urlTmp
                if not pageUrl in self.gzhPageSet:

                    # add to set and file
                    self.gzhPageSet.add(pageUrl)
                    with open("gzhPageSet.txt",'a') as ff:
                        ff.write(pageUrl+"\n")

                    r1 = requests.get(pageUrl)
                    print("http://" +urlTmp)
                    soup1 = BeautifulSoup(r1.text)
                    div1 = soup1.find("div",{"class":"resourcese"})
                    for li in div1.find_all("li",{"class":"author-item-li"}):
                        try:
                            a = li.find("a")
                            href = a.get("href")
                            finalUrl = self.webSiteUrl+href
                            self.crawRengzanGZHDetails(finalUrl,ctg)
                        except Exception,e:
                            print("Second level exception" + str(e))
                            continue
                        #break
                else:
                    continue
            except Exception:
                continue
            #break

    def crawRengzanGZHDetails(self,url,ctg):
        r = requests.get("http://" +url)
        soup = BeautifulSoup(r.text)
        div = soup.find("div",{"class":"cont"})
        resultsLis = div.find_all("li")
        weixinNameLiStr = resultsLis[0].getText().split('\n')[2].strip()
        weixinAccountLiStr = resultsLis[1].getText().split('\n')[2].strip()

        newGzhObj = WeixinAccount()
        newGzhObj.accountName = weixinNameLiStr.encode("utf-8")
        newGzhObj.aid = weixinAccountLiStr.encode("utf-8")
        newGzhObj.category = ctg#.decode('utf-8').encode('utf-8')
        newGzhObj.url = url

        if(weixinAccountLiStr in self.ghzSet):
            print(weixinAccountLiStr + u"重复")
            print("\n")
            return
        else:
            self.ghzSet.add(weixinAccountLiStr)
            with open("gzhAccoutSet.txt",'a') as ff:
                ff.write(weixinAccountLiStr+"\n")
            self.finalResultList.append(newGzhObj.__dict__)

            print(newGzhObj.__dict__)

        print(newGzhObj.accountName)
        print(newGzhObj.aid)
        print(newGzhObj.category)
        print(newGzhObj.url)
        with open("results.txt",'a') as ff:
            resultStr = newGzhObj.accountName+","+newGzhObj.aid+","+newGzhObj.url.encode("utf-8")+","+newGzhObj.category+","+str(newGzhObj.total_articles)+","+str(newGzhObj.last_week_read)+","+newGzhObj.last_modified_date+"\n"
            #newGzhObj.category
            ff.write(resultStr)

        self.totalNumber+=1
        print("total = " + str(self.totalNumber))
        print("\n\n")


    def ctgMapping(self,ctg):
        output = ""
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
        if ctg == u"新闻": output="时事·城市"
        return output




a = gzhRengZan()
a.crawlRengZan()