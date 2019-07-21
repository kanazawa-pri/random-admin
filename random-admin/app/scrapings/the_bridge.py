from bs4 import BeautifulSoup
import requests
import random
import re

def scraping():
    ng_list = ["the bridge"]
    html = requests.get('https://thebridge.jp/')
    soup = BeautifulSoup(html.text, "html.parser")
    article = soup.find(class_="articles")
    title = article.find(class_="entry-title").string
    for i in ng_list:
        if i in title:
            return
    reporter = ''
    try:
        reporter = soup.find(class_="text-muted").text
        reporter = reporter[4:]
    except:
        print("reporter not found")
    image = soup.find(class_="entry-thumbnail")
    image = image.a.get("style")
    url = article.a.get("href")
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    soup = soup.find(class_="post-body")
    text = ''.join([s.text for s in soup.find_all("p")])
    return {'article_text':text,'article_title':title, 'article_url':url,'article_reporter':reporter.split('\n')[0], 'site_name':'the_bridge','article_image': image.split('url(')[1][:-1]}

if __name__ == "__main__":
    print(scraping())
