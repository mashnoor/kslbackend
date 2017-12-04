import grequests, json, requests

from bs4 import BeautifulSoup
from helpers import get_column_values

with open("all_company_info.txt", "r") as f:
    all_items_info = json.load(f)

item_detail_urls = []
item_company_names = []
for item_info in all_items_info:
    item_detail_urls.append(item_info['link'])
    item_company_names.append(item_info['scd'])




#req = (grequests.get(url) for url in item_detail_urls)

responses = []
#responses = grequests.map(req)
for url in item_detail_urls:
    print(url)
    r = requests.get(url)
    responses.append(r)




for idx, response in enumerate(responses):



    soup = BeautifulSoup(response.content, 'lxml')
    table_attrs = {"width":"100%", "border":"0", "cellpadding":"0", "cellspacing":"0"}
    table = soup.find_all("table", table_attrs)

    current_item_info = {}  # Store all the info of the company

    ############# Parse Current Market Info Table ############

    inner_tables = table[2].find_all("table")
    current_item_info.update(get_column_values(str(inner_tables[0]), ['ltp', 'ltd', 'change', 'openprice', 'range']))
    current_item_info.update(get_column_values(str(inner_tables[1]), ['trade', 'volume', 'closeprice', 'ycp', 'capital']))
    with open("item_details/" + item_company_names[idx] + ".txt", "w") as f:
        f.write(json.dumps(current_item_info))
    print(current_item_info)
