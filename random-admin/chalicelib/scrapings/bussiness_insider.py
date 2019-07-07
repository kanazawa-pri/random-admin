from bs4 import BeautifulSoup
import requests
import random

ng_list = []

def scraping(ng_list):

    html = requests.get('https://www.businessinsider.jp/')
    soup = BeautifulSoup(html.text, "html.parser")
    soup = soup.find_all(class_="p-cardList-cardTitle")
    cnt = 0
    while cnt < 5:
        article = random.choice(soup)
        if any(s in article for s in ng_list):
            cnt += 1
            continue 
        break
    
    url = 'https://www.businessinsider.jp' + article.a.get("href")
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    text = ''.join([s.text for s in soup.find_all(class_="p-post-content")])
    return {'text':text, 'url':url}

if __name__ == "__main__":
    print(scraping(['アニメ']))