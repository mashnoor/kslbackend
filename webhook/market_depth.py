import json

from flask import Blueprint, request

import requests
from bs4 import BeautifulSoup
from datetime import datetime

market_depth_api = Blueprint('market_depth_api', __name__)


@market_depth_api.route('/getbuymarketdepth/<item>')
def getBuyMarketDepth(item):
    url = "http://www.cse.com.bd/depth_show.php?w=" + item + "&sid=0.6294890369546924"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    attrs = {"width": "96%", "border": "0", "align": "left", "cellpadding": "0", "cellspacing": "0",
             "bgcolor": "#E8FFFB"}
    table = soup.find_all("table", attrs=attrs)[0]

    i = 0
    buy_depths = []
    for tr in table.find_all("tr"):
        if i < 2:
            i += 1
            continue

        # print(tr)
        td = tr.find_all("td")
        curr_depth = {}
        curr_depth['price'] = str(td[0].text).strip()
        curr_depth['volume'] = str(td[2].text).strip()
        buy_depths.append(curr_depth)

    return json.dumps(buy_depths)


@market_depth_api.route('/getsellmarketdepth/<item>')
def getSellMarketDepth(item):
    url = "http://www.cse.com.bd/depth_show.php?w=" + item + "&sid=0.6294890369546924"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    attrs = {"width": "96%", "border": "0", "align": "left", "cellpadding": "0", "cellspacing": "0"}
    table = soup.find_all("table", attrs=attrs)[1]
    

    i = 0
    sell_depths = []
    for tr in table.find_all("tr"):
        if i < 2:
            i += 1
            continue

        # print(tr)
        td = tr.find_all("td")
        curr_depth = {}
        curr_depth['price'] = str(td[0].text).strip()
        curr_depth['volume'] = str(td[2].text).strip()
        sell_depths.append(curr_depth)

    return json.dumps(sell_depths)
