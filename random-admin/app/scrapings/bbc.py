from bs4 import BeautifulSoup
import requests
import random
import re

def scraping():
    ng_list = ["bbc"]
    html = requests.get('https://www.bbc.com/japanese')
    soup = BeautifulSoup(html.text, "html.parser")
    article = soup.find(class_="pigeon__column pigeon__column--a")
    title = article.find(class_="title-link__title-text").string
    for i in ng_list:
        if i in title:
            return
    image = article.find(class_="js-delayed-image-load")
    print(image)
    image = image.get("data-src")
    url = "https://www.bbc.com/" + article.a.get("href")
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    soup = soup.find(class_="story-body__inner")
    text = ''.join([s.text for s in soup.find_all("p")])
    return {'article_text':text,'article_title':title, 'article_url':url,'article_reporter':'', 'site_name':'bbc','article_image': image}

if __name__ == "__main__":
    print(scraping())











