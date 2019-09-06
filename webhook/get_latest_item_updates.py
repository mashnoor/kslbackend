from bs4 import BeautifulSoup

import json
from flask import Blueprint
import time
import settings

if settings.use_fast_requests:
    import faster_than_requests as req
else:
    import requests

get_latest_item_updates_api = Blueprint('get_latest_item_updates_api', __name__)
url = "https://www.cse.com.bd/market/current_price"


@get_latest_item_updates_api.route('/getlatestitems')
def getlatestitems():
    if settings.use_fast_requests:
        html = req.get2str(url)
    else:
        r = requests.get(url, verify=False)
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
            open = float(inner_data[3].get_text().strip())

            change_percentage = ((ltp - open) / open) * 100.0
            change_percentage = str(format(change_percentage, '.2f') + "%")
        except:
            pass

        curr_item['changepercentage'] = change_percentage
        all_items.append(curr_item)

    return json.dumps(all_items)
