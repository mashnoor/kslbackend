from bs4 import BeautifulSoup
from orderstatus import status
from flask import Blueprint, render_template, request
import json

getorderstatus_api = Blueprint('orderstatus_api', __name__)


@getorderstatus_api.route("/getorderstatus", methods=["POST"])
def getorderstatus():
    its_id = request.form.get("itsaccountno")
    its_pass = request.form.get("itsaccountpass")
    start_date = request.form.get("startdate")
    end_date = request.form.get("enddate")

    statushtml = status(its_id, its_pass, start_date, end_date)

    print(statushtml)

    if statushtml == "NOTOK":
        return "NOTOK"
    soup = BeautifulSoup(statushtml, 'html.parser')

    table_attrs = {"id": "searchtable", "style": "width:100% ;valign=top", "class": "tableheading"}

    orders = []
    keys = ["symbol", "boardtype", "scripgroup", "orderno", "settlor", "exch",
            "bs", "orderqty", "price", "minfillqty", "executedqty",
            "pricetype", "avgprice", "time", "status", "mc"]

    table = soup.find("table", attrs=table_attrs)

    try:

        for tr in table.find_all("tr"):
            curr_order = []
            for td in tr.find_all("td"):
                curr_order.append(str(td.text).strip())
            orders.append(dict(zip(keys, curr_order)))

        del orders[0]
        orders.reverse()
        return json.dumps(orders)
    except:
        return "ERROR"
