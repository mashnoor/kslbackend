from bs4 import BeautifulSoup
import requests
import json
from flask import Blueprint

get_latest_item_updates_api = Blueprint('get_latest_item_updates_api', __name__)
url = "https://www.cse.com.bd/market/current_price"

@get_latest_item_updates_api.route('/getlatestitems')
def getlatestitems():
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

    return json.dumps(all_items)
