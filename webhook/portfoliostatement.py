from flask import Blueprint, render_template, request
import dbhelper, json
import requests


portfoliostatement_api = Blueprint('portfoliostatement_api', __name__)

ps_api = 'http://api.kslbd.net:88/client/report/ps/select/sandbox/sandbox/sandbox/'

@portfoliostatement_api.route('/getportfoliostatement', methods=['POST'])
def getportfoliostatement():

    client_id = request.form.get('client_id')
    portfolio_date = request.form.get('portfolio_date')
    print(client_id)
    print(portfolio_date)
    json_str = json.dumps({
        'portfolio_date':portfolio_date,
        'client_id':client_id
    })
    r = requests.get(ps_api + json_str)
    return str(r.text)