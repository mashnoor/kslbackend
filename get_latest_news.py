import requests, json
from bs4 import BeautifulSoup
import re

url = "http://cse.com.bd/news_details.php"

r = requests.get(url)

soup = BeautifulSoup(r.content, 'lxml')
news_table_attrs = {"id":"report", "width":"100%", "border":"0", "cellspacing":"0", "cellpadding":"0"}
news_table = soup.find("table", news_table_attrs)

news_list = soup.find_all("tr",re.compile("TZRow"))


all_news = []
for news in news_list:
   try:

       title = news.find("b").get_text().strip()
       body = news.get_text().replace(title, "").strip()
       curr_news = {}
       curr_news["title"] = title
       curr_news["body"] = body
       all_news.append(curr_news)
   except:
       pass

with open("latest_news.txt", "w") as f:
    f.write(json.dumps(all_news))