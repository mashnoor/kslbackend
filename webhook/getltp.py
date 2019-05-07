import pandas as pd
from trade import buy_item

from flask import Flask, request, Blueprint

url = "http://www.cse.com.bd"
app = Flask(__name__)
get_ltp_api = Blueprint('get_ltp_api', __name__)


@get_ltp_api.route('/getltp/<item>')
def getltp(item):
    df = pd.read_html(url, attrs={'border': '0', 'cellspacing': '0', 'cellpadding': '0'})
    total_items = len(df)

    for i in range(1, total_items):
        curr_item = df[i][1][0]
        if str(curr_item) == str(item):
            return df[i][1][1]

    return "null"


@get_ltp_api.route('/trade', methods=['POST'])
def trade():
    login_id = request.form.get('loginid')
    password = request.form.get('password')
    item = request.form.get('item')
    qty = request.form.get('qty')
    return buy_item(login_id, password, item, qty, getltp(item))
