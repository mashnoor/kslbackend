from bs4 import BeautifulSoup
import requests
import json
from flask import Blueprint

url = "https://www.cse.com.bd/media/news"

r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')
news_div_attrs = {"class": "news_content"}
news_divs = soup.find_all("div", news_div_attrs)

all_news = []
for news in news_divs:
    try:
        all_paragraphs = news.find_all("p")
        first_p = all_paragraphs[0]
        second_p = all_paragraphs[1]

        curr_news = {}
        curr_news["title"] = str(first_p.text).split(":")[1].strip()
        curr_news["body"] = str(second_p.text).strip()
        curr_news['date'] = str(first_p.text).split(":")[0].strip()
        all_news.append(curr_news)
    except:
        pass

with(open('latest_news.txt', 'w')) as f:
    f.write(json.dumps(all_news))
