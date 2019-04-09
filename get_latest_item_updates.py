import requests, json
from bs4 import BeautifulSoup

url = "https://www.cse.com.bd/market/current_price"

r = requests.get(url, verify=False)

soup = BeautifulSoup(r.content, 'html.parser')



all_items_table = soup.find("tbody")
print(all_items_table)
all_items = []
for item in all_items_table.find_all("tr"):
    inner_data = item.find_all('td')
    curr_item = {}
    curr_item['item'] = inner_data[1].get_text().strip()
    curr_item['ltp'] = inner_data[2].get_text().strip()
    curr_item['changeval'] = inner_data[8].get_text().strip()
    curr_item['volume'] = inner_data[9].get_text().strip()
    all_items.append(curr_item)


print(all_items)
with open('all_items_latest_update.txt', 'w') as f:
    f.write(json.dumps(all_items))
