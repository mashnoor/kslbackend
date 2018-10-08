import requests, json
from bs4 import BeautifulSoup

url = "https://www.cse.com.bd/market/current_price"

r = requests.get(url, verify=False)

soup = BeautifulSoup(r.content, 'html5lib')

div_attrs = {"class": "market_tabs_cont"}

all_item_divs = soup.find_all("div", div_attrs)
all_items = []
for item in all_item_divs:
    inner_divs = item.find_all('div')
    curr_item = {}
    curr_item['item'] = inner_divs[1].get_text().strip()
    curr_item['ltp'] = inner_divs[2].get_text().strip()
    curr_item['changeval'] = inner_divs[7].get_text().strip()
    curr_item['volume'] = inner_divs[9].get_text().strip()
    all_items.append(curr_item)


print(all_items)
with open('all_items_latest_update.txt', 'w') as f:
    f.write(json.dumps(all_items))
