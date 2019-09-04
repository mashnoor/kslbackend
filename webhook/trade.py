import requests
from bs4 import BeautifulSoup
from flask import Blueprint, request
import dbhelper

trade_api = Blueprint('trade_api', __name__)

url = "https://bangladeshstockmarket.com/LoadBalance.do"

order1url = "https://bangladeshstockmarket.com/Order1.do?exchangeSelected=CTG"

verifyPassword = "https://bangladeshstockmarket.com/PasswordCheck.do"


@trade_api.route('/trade', methods=['POST'])
def buy_item():
    loginid = request.form.get('loginid')
    password = request.form.get('password')
    symbol = request.form.get('symbol')
    qty = request.form.get('qty')
    price = request.form.get('price')
    verb = request.form.get('verb')
    print(loginid)
    print(password)
    d = {'loginid': loginid, 'password': password, 'lang1': 'default'}
    order1_data = {'spdBuySymbol': '', 'spdSellSymbol': '', 'submitbutton': 'Submit', 'exchange': 'CTG',
                   'selectProduct': 'EQUITY', 'segment': 'DELIVERY', 'symbol': symbol, 'buysell': verb,
                   'quantity': qty, 'referenceId': '', 'pricetype': 'LIMIT', 'price': price, 'triprice': '0',
                   'disquan': '', 'protectionPercent': '', 'filltype': 'GFD', 'minFillQty': '',
                   'expirydate': '', 'settlerid': '', 'priceViolation': 'N', 'lotsize': '1', 'userExchangeList': 'CTG',
                   'hidboardtype': 'NR'}

    with requests.Session() as s:
        r = s.post(url, data=d)
        # print r.text
        r = s.post(verifyPassword, data={'pagePassword': password})
        if (r.text == "NOTOK"):
            return "ITS Login Failed!"
        r = s.post(order1url, data=order1_data)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.find_all('font')[0].text
        # with open('data.txt', 'w+') as f:
        #   f.write(r.text)
