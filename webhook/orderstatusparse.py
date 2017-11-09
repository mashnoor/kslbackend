from bs4 import BeautifulSoup
from orderstatus import status
from flask import Blueprint, render_template, request

getorderstatus_api = Blueprint('orderstatus_api', __name__)
@notification_api.route("/getorderstatus", methods = ["POST"])
def getorderstatus():
    req_json = request.get_json()
    its_id = req_json["itsaccountno"]
    its_pass = req_json["itsaccountpass"]


    statushtml = status(its_id, its_pass)

    soup = BeautifulSoup(statushtml, 'lxml')

    table_attrs = {"id":"searchtable", "style":"width:100% ;valign=top", "class":"tableheading"}

    orders = []
    keys = ["symbol", "boardtype", "scripgroup", "orderno", "settlor", "exch",
        "bs", "orderqty", "price", "minfillqty", "executedqty",
        "pricetype", "avgprice", "time", "status", "mc"]

    table = soup.find("table", attrs=table_attrs)

    for tr in table.find_all("tr"):
        curr_order = []
        for td in table.find_all("td"):
            curr_order.append(str(td.text).strip())
        orders.append(dict(zip(keys, curr_order)))

    return orders
