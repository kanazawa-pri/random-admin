from bs4 import BeautifulSoup
import requests
import random
import re

def scraping():
    ng_list = ["bussiness insider"]
    html = requests.get('https://www.businessinsider.jp/')
    soup = BeautifulSoup(html.text, "html.parser")
    article = soup.find(class_="p-cardList")
    title = article.find(class_="p-cardList-cardTitle").string
    for i in ng_list:
        if i in title:
            return
    image = soup.find(class_="p-cardList-cardImage")
    image = image.img.get("src")
    url = "https://www.businessinsider.jp/" + article.a.get("href")
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    reporter = ''
    try:
        reporter = soup.find(class_="p-post-bylineAuthor").text
    except:
        print("reporter not found")
    main = soup.find(class_="p-post-content")
    text = ''.join([s.text for s in main.find_all("p")])
    return {'article_text':text,'article_title':title, 'article_url':url,'article_reporter':reporter.replace(' ［Business Insider Japan］ ','') ,'site_name':'bussiness_insider','article_image': image}

if __name__ == "__main__":
    print(scraping())
