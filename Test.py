__author__ = 'chhe'

from bs4 import BeautifulSoup
import requests
from gzhPojo import WeixinAccount
import re
import json

url = "www.rengzan.com//weixin-show-id-28857.html"
r = requests.get("http://" +url)
soup = BeautifulSoup(r.text)
div = soup.find("div",{"class":"cont"})
resultsLis = div.find_all("li")
weixinNameLiStr = resultsLis[0].getText().split('\n')[2].strip()
weixinAccountLiStr = resultsLis[1].getText().split('\n')[2].strip()

newGzhObj = WeixinAccount()
newGzhObj.accountName = weixinNameLiStr.encode("utf-8")
newGzhObj.aid = weixinAccountLiStr.encode("utf-8")
newGzhObj.url = url

print(newGzhObj.accountName)
print(newGzhObj.aid)

print(newGzhObj.category)

print(newGzhObj.url)