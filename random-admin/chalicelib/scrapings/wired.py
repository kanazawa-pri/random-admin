from bs4 import BeautifulSoup
import requests
import random

def scraping():
    ng_list = ["wired"]
    html = requests.get('https://wired.jp')
    soup = BeautifulSoup(html.text, "html.parser")
    article = soup.find(class_="listed-article-norm")
    
    title = article.h3.string
    url = article.a.get("href")
    image = article.img.get("data-original")
    html = requests.get(url)
    print(url)
    soup = BeautifulSoup(html.text, "html.parser")
    soup = soup.find(class_="article-detail")
    text = ''.join([s.text for s in soup.find_all('p')])
    return {'article_text':text,'article_title':title, 'article_url':url, 'site_name':'wired','article_image': image}

if __name__ == "__main__":
    print(scraping())
