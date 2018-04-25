from flask import Blueprint, render_template, request, redirect, url_for
import dbhelper
import json
import requests
financial_ledger_api = Blueprint('financial_ledger_api', __name__)


url = "http://api.kslbd.net:88/client/report/sfla/select/sandbox/sandbox/sandbox/"

@financial_ledger_api.route("/getfinancialledgrs", methods=["POST"])
def getFinancialLedgers():
    client_id = request.form.get('client_id')
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    vals = {'from_date': from_date, 'to_date': to_date, 'client_id': client_id}
    print(vals)
    r = requests.get(url + json.dumps(vals))
    print(r.content)
    res_json = r.json()
    return json.dumps(res_json["_ret_data_table"][0]["detail"])
