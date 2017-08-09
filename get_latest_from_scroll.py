import requests, json
from bs4 import BeautifulSoup

url = "http://cse.com.bd/current_share_price_tc.php"

r = requests.get(url)

soup = BeautifulSoup(r.content, 'lxml')

table_attrs = {"id":"report", "width":"100%", "border":"0", "cellpadding":"0", "cellspacing":"0", "bgcolor":"#355DA2"}

table = soup.find("table", table_attrs)
all_items = []
for tr in table.find_all("tr"):
    td = tr.find_all("td")
    curr_item = {}
    curr_item['item'] = td[1].get_text().strip()
    curr_item['ltp'] = td[2].get_text().strip()
    curr_item['change'] = td[7].get_text().strip()
    curr_item['volume'] = td[9].get_text().strip()
    all_items.append(curr_item)

del(all_items[0])

with open('all_items_latest_update.txt', 'wb') as f:
    f.write(json.dumps(all_items))
