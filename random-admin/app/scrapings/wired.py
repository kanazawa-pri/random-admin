from bs4 import BeautifulSoup
import requests
import random

def scraping():
    ng_list = ["wired"]
    html = requests.get('https://wired.jp')
    soup = BeautifulSoup(html.text, "html.parser")
    article = soup.find(class_="listed-article-norm")
    title = article.h3.string
    for i in ng_list:
        if i in title:
            return
    url = article.a.get("href")
    image = article.img.get("data-original")
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    main = soup.find(class_="article-detail")
    head = soup.find(class_="contents-main")
    reporter = ''
    try:
        reporter = head.find(class_="post-credit").text
        reporter = reporter.split("\r\n")[0]
    except:
        print("reporter not found")
    text = ''.join([s.text for s in main.find_all('p')])
    return {'article_text':text,'article_title':title, 'article_url':url,'article_reporter':reporter.replace("TEXT BY ", ""), 'site_name':'wired','article_image': image}

if __name__ == "__main__":
    print(scraping())
