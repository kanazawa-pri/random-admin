from bs4 import BeautifulSoup
import requests
import random
import re

def scraping():
    ng_list = ["デジモン","gigazine","予告","開催中"]
    html = requests.get('https://gigazine.net/')
    soup = BeautifulSoup(html.text, "html.parser")
    article = soup.find("h2")
    title = article.span.string
    for i in ng_list:
        if i in title:
            return
    image = soup.find(class_="thumb")
    image = image.img.get("src")
    url = article.a.get("href")
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    text = ''.join([s.text for s in soup.find_all(class_="preface")])
    return {'article_text':text,'article_title':title, 'article_url':url, 'site_name':'gigazine','article_image': image}

if __name__ == "__main__":
    print(scraping())
