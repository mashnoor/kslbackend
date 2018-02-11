from bs4 import BeautifulSoup
import requests, json
from flask import Blueprint

get_item_news_api = Blueprint('get_item_news_api', __name__)

url = "http://www.dsebd.org/old_news.php"


@get_item_news_api.route('/getitemnews/<company_name>')
def getItemNews(company_name):
    r = requests.post(url, data={"cboSymbol": company_name})
    html = BeautifulSoup(r.text, "html.parser")
    params = {"border": "0", "cellspacing": "3", "width": "100%"}
    tables = html.find_all("table", params)

    all_news = []
    for table in tables:
        rows = table.find_all("tr")
        curr_news = {}
        curr_news["body"] = rows[1].text.replace("News:", "")
        curr_news["date"] = rows[2].text.replace("Post Date:", "")

        all_news.append(curr_news)

    return json.dumps(all_news)
