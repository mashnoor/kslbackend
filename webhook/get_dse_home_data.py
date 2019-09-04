from bs4 import BeautifulSoup
import requests
import json
from flask import Blueprint

get_dse_home_data_api = Blueprint('get_dse_home_data_api', __name__)


@get_dse_home_data_api.route('/dsehomedata')
def dsehomedata():
    response = requests.get("http://dsebd.org/index.php")

    res_str = str(response.text)

    # print source

    soup = BeautifulSoup(res_str, 'html.parser')
    alldivs = soup.find_all('div', attrs={'class': 'midrow'})

    result = {}

    # DSEX
    curr_divs = alldivs[0].find_all('div')
    result['dsex_data1'] = str(curr_divs[1].text).strip()
    result['dsex_data2'] = str(curr_divs[2].text).strip()
    result['dsex_data3'] = str(curr_divs[3].text).strip()

    # DSES
    curr_divs = alldivs[1].find_all('div')
    result['dses_data1'] = str(curr_divs[1].text).strip()
    result['dses_data2'] = str(curr_divs[2].text).strip()
    result['dses_data3'] = str(curr_divs[3].text).strip()

    # DS30
    curr_divs = alldivs[2].find_all('div')
    result['ds30_data1'] = str(curr_divs[1].text).strip()
    result['ds30_data2'] = str(curr_divs[2].text).strip()
    result['ds30_data3'] = str(curr_divs[3].text).strip()

    # Total Data
    curr_divs = alldivs[4].find_all('div')
    result['total_trade'] = str(curr_divs[0].text).strip()
    result['total_volume'] = str(curr_divs[1].text).strip()
    result['total_value'] = str(curr_divs[2].text).strip()

    # All Issue Data
    curr_divs = alldivs[6].find_all('div')
    result['issues_advanced'] = str(curr_divs[0].text).strip()
    result['issues_declined'] = str(curr_divs[1].text).strip()
    result['issues_unchanged'] = str(curr_divs[2].text).strip()

    # marketStatus
    marketstatus = soup.find("span", {"class": "time"})
    result['date'] = str(marketstatus.text).strip()


    return json.dumps(result)
