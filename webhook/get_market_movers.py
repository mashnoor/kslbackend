from bs4 import BeautifulSoup
import requests
import json
from flask import Blueprint

get_market_movers_api = Blueprint('get_market_movers_api', __name__)
url = "https://www.cse.com.bd"

########## Value #############
@get_market_movers_api.route('/getmarketmovers/byvalue')
def getMarketMoversByValue():
    r = requests.get(url, verify=False)

    soup = BeautifulSoup(r.content, 'html.parser')

    div_attr = {"class": "mover_tap_content "}
    top_mover_by_value_div = soup.find("div", div_attr)
    top_twenty_by_value = []
    for div in top_mover_by_value_div.find_all('div', {'class': "immover_MIrow1"}):
        inner_divs = div.find_all('div')
        curr_item = {}
        curr_item['item'] = inner_divs[0].get_text().strip()
        curr_item['ltp'] = inner_divs[1].get_text().strip()
        curr_item['value'] = inner_divs[4].get_text().strip()
        top_twenty_by_value.append(curr_item)

    return json.dumps(top_twenty_by_value)


########### Volume ##########
@get_market_movers_api.route('/getmarketmovers/byvolume')
def getMarketMoversByVolume():
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    div_attr = {"class": "mover_tap_content"}
    top_mover_by_volume_div = soup.find_all("div", div_attr)[1]
    top_twenty_by_volume = []
    for div in top_mover_by_volume_div.find_all('div', {'class': "immover_MIrow1"}):
        inner_divs = div.find_all('div')
        curr_item = {}
        curr_item['item'] = inner_divs[0].get_text().strip()
        curr_item['ltp'] = inner_divs[1].get_text().strip()
        curr_item['volume'] = inner_divs[4].get_text().strip()
        top_twenty_by_volume.append(curr_item)

    return json.dumps(top_twenty_by_volume)


############## Trade ##############
@get_market_movers_api.route('/getmarketmovers/bytrade')
def getMarketMoversByTrade():
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    div_attr = {"class": "mover_tap_content"}
    top_mover_by_trade_div = soup.find_all("div", div_attr)[2]
    top_twenty_by_trade = []
    for div in top_mover_by_trade_div.find_all('div', {'class': "immover_MIrow1"}):
        inner_divs = div.find_all('div')
        curr_item = {}
        curr_item['item'] = inner_divs[0].get_text().strip()
        curr_item['ltp'] = inner_divs[1].get_text().strip()
        curr_item['trade'] = inner_divs[4].get_text().strip()
        top_twenty_by_trade.append(curr_item)

    return json.dumps(top_twenty_by_trade)
