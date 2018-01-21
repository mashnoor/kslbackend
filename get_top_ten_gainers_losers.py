from bs4 import BeautifulSoup
import requests, json

top_ten_gainer_url = "http://www.dse.com.bd/top_ten_gainer.php"
top_ten_losers_url = "http://www.dse.com.bd/top_ten_loser.php"

r = requests.get(top_ten_gainer_url)
soup = BeautifulSoup(r.content, "html.parser")

table = soup.find("table",
                  attrs={"border": "0", "cellpadding": "3", "width": "100%", "bgcolor": "#808000", "cellspacing": "1"})
top_gainers = []
for tr in table.find_all("tr"):
    curr_gainer = {}
    td = tr.find_all("td")
    curr_gainer["item"] = str(td[1].text).replace("\r\n", "").strip()
    curr_gainer["closeprice"] = str(td[2].text).replace("\r\n", "").strip()
    curr_gainer["high"] = str(td[3].text).replace("\r\n", "").strip()
    curr_gainer["low"] = str(td[4].text).replace("\r\n", "").strip()
    curr_gainer["closeprice"] = str(td[5].text).replace("\r\n", "").strip()
    curr_gainer["change"] = str(td[6].text).replace("\r\n", "").strip()
    top_gainers.append(curr_gainer)
del top_gainers[0]
with open("top_gainers.txt", "w") as f:
    f.write(json.dumps(top_gainers))


r = requests.get(top_ten_losers_url)
soup = BeautifulSoup(r.content, "html.parser")

table = soup.find("table",
                  attrs={"border": "0", "cellpadding": "3", "width": "100%", "bgcolor": "#808000", "cellspacing": "1"})
top_losers = []
for tr in table.find_all("tr"):
    curr_loser = {}
    td = tr.find_all("td")
    curr_loser["item"] = str(td[1].text).replace("\r\n", "").strip()
    curr_loser["closeprice"] = str(td[2].text).replace("\r\n", "").strip()
    curr_loser["high"] = str(td[3].text).replace("\r\n", "").strip()
    curr_loser["low"] = str(td[4].text).replace("\r\n", "").strip()
    curr_loser["closeprice"] = str(td[5].text).replace("\r\n", "").strip()
    curr_loser["change"] = str(td[6].text).replace("\r\n", "").strip()
    top_losers.append(curr_loser)

del top_losers[0]
with open("top_losers.txt", "w") as f:
    f.write(json.dumps(top_losers))
