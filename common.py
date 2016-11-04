__author__ = 'chhe'
from weikou_article import WeikouArticle
from project.http.requests.proxy.requestProxy import RequestProxy
from bs4 import BeautifulSoup
import requests,json,string



def getWeikouArticleObj(href,req_proxy):
    weikou_article_obj = WeikouArticle()
    resp = req_proxy.generate_proxied_request(href)
    page_soup = BeautifulSoup(resp.text)
    article_page_div = page_soup.find("div", {"class":"articleContainer"})

    title = article_page_div.find('h1').text.strip()
    author_div = article_page_div.find("div", {"class":"author-name"})
    author_link = author_div.find('a')['href']
    author_name = author_div.find('a',{"class":"art-cont-name fl"}).text.strip()
    main_article =  page_soup.find("div", {"class":"article-cont"})
    image_urls = main_article.findAll('img')
    image_url = image_urls[0]["data-echo"].split("url=")[1]

    weikou_article_obj.title = title
    weikou_article_obj.author_link = author_link
    weikou_article_obj.author_name = author_name
    weikou_article_obj.image_url = image_url

    print(title)
    article_content = article_page_div.find("div",{"class" : "article-cont"})
    content = ""

    image_tag = """<media>{"type":"%s","url":"%s"}</media>"""

    hasSetIntro = False
    try:
    	for p in article_content.findAll('p'):
            if p.find(lambda tag: tag.name == 'img' and 'data-echo' in tag.attrs):
                media_type = p.find('img')["data-echo"].split("wx_fmt=")[1]
                media_src = p.find('img')["data-echo"].split("url=")[1].split('?')[0]
                media_line = image_tag % (media_type,media_src)
                print(media_line)
                content += '\n'+media_line
            else:
				content += '\n' + p.text
				if not hasSetIntro:
					weikou_article_obj.intro = p.text
					hasSetIntro = True
    except:
        print("image parsing error:"+href)
        return

    weikou_article_obj.content = content
    return weikou_article_obj