from bs4 import BeautifulSoup
import requests
import random
import re

def scraping():
    ng_list = ["デジモン","gigazine","予告","開催中"]
    html = requests.get('https://note.mu/')
    soup = BeautifulSoup(html.text, "html.parser")
    article = soup.find(class_="o-timeline__item")
    title = article.find(class_="o-textNote__title").string
    for i in ng_list:
        if i in title:
            return
    reporter = ''
    try:
        reporter = soup.find(class_="o-timelineFooter__name").string
    except:
        print("reporter not found")
    image = soup.find(class_="o-textNote__eyecatch is-first")
    image = image.img.get("src")
    url = "https://note.mu/" + article.a.get("href")
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    text = ''.join([s.text for s in soup.find(class_="o-noteContentText__body")])
    return {'article_text':text,'article_title':title.strip(), 'article_url':url,'article_reporter':reporter, 'site_name':'note','article_image': image}

if __name__ == "__main__":
    print(scraping())
