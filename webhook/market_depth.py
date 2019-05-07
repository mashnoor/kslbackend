import json

from flask import Blueprint, request

import requests
from bs4 import BeautifulSoup
from datetime import datetime

market_depth_api = Blueprint('market_depth_api', __name__)


@market_depth_api.route('/getmarketdepth/<item>')
def getBuyMarketDepth(item):
    final_depth = dict()
    url = "https://www.cse.com.bd/market/market_depth/" + item

    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")

    attrs = {"class": "bodycol_6 aci_header"}
    all_divs = soup.find_all("div", attrs=attrs)

    buy_price_divs = all_divs[0]
    buy_volume_divs = all_divs[1]
    sell_price_divs = all_divs[2]
    sell_volume_divs = all_divs[3]

    buy_prices_depth = []
    sell_prices_depth = []

    buy_price_divs = buy_price_divs.find_all('div')
    buy_volume_divs = buy_volume_divs.find_all('div')
    sell_price_divs = sell_price_divs.find_all('div')
    sell_volume_divs = sell_volume_divs.find_all('div')
    for i in range(len(buy_price_divs)):
        curr_depth = dict()
        if str(buy_price_divs[i].text).strip() == "Buy Price":
            continue
        curr_depth['price'] = str(buy_price_divs[i].text).strip()
        curr_depth['volume'] = str(buy_volume_divs[i].text).strip()
        buy_prices_depth.append(curr_depth)

    for i in range(len(sell_price_divs)):
        curr_depth = dict()
        if str(sell_price_divs[i].text).strip() == "Sell Price":
            continue
        curr_depth['price'] = str(sell_price_divs[i].text).strip()
        curr_depth['volume'] = str(sell_volume_divs[i].text).strip()
        sell_prices_depth.append(curr_depth)

        # del (buy_prices_depth[0]
        # del sell_prices_depth[0]
        final_depth['buy'] = buy_prices_depth
        final_depth['sell'] = sell_prices_depth

    return json.dumps(final_depth)
