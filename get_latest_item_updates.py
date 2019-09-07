from bs4 import BeautifulSoup

import json
import requests

url = "https://www.cse.com.bd/market/current_price"

r = requests.get(url)
html = r.content

soup = BeautifulSoup(html, 'html.parser')

all_items_table = soup.find("tbody")
print(all_items_table)
all_items = []
for item in all_items_table.find_all("tr"):
    inner_data = item.find_all('td')
    curr_item = {}
    curr_item['item'] = inner_data[1].get_text().strip()
    curr_item['ltp'] = inner_data[2].get_text().strip()
    curr_item['volume'] = inner_data[9].get_text().strip()

    # Change Percentage Calculation
    change_percentage = "--"
    try:
        ltp = float(inner_data[2].get_text().strip())
        oepnPrice = float(inner_data[3].get_text().strip())

        change_percentage = ((ltp - oepnPrice) / oepnPrice) * 100.0
        change_percentage = str(format(change_percentage, '.2f') + "%")
    except:
        pass

    curr_item['changepercentage'] = change_percentage
    all_items.append(curr_item)

with(open('all_items_latest_update.txt', 'w')) as f:
    f.write(json.dumps(all_items))
