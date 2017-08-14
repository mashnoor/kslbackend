import requests, json
from bs4 import BeautifulSoup

url = "http://www.cse.com.bd/market_movers.php"

r = requests.get(url)

soup = BeautifulSoup(r.content, 'lxml')

table_attrs = {"id":"report", "width":"100%", "border":"0", "cellpadding":"0", "cellspacing":"0", "bgcolor":"#355DA2"}

tables = soup.find_all("table", table_attrs)

########### Volume ##########
top_twenty_by_volume = []
for tr in tables[0].find_all('tr'):
    td = tr.find_all('td')
    curr_item = {}
    curr_item['item'] = td[1].get_text().strip()
    curr_item['ltp'] = td[2].get_text().strip()
    curr_item['volume'] = td[9].get_text().strip()
    top_twenty_by_volume.append(curr_item)

del(top_twenty_by_volume[0])
with open('marketmovers/top_twenty_by_volume.txt', 'wb') as f:
    f.write(json.dumps(top_twenty_by_volume))


########## Value #############
top_twenty_by_value = []
for tr in tables[1].find_all('tr'):
    td = tr.find_all('td')
    curr_item = {}
    curr_item['item'] = td[1].get_text().strip()
    curr_item['ltp'] = td[2].get_text().strip()
    curr_item['value'] = td[7].get_text().strip()
    top_twenty_by_value.append(curr_item)

del(top_twenty_by_value[0])
with open('marketmovers/top_twenty_by_value.txt', 'wb') as f:
    f.write(json.dumps(top_twenty_by_value))


############## Trade ##############
top_twenty_by_trade = []
for tr in tables[2].find_all('tr'):
    td = tr.find_all('td')
    curr_item = {}
    curr_item['item'] = td[1].get_text().strip()
    curr_item['ltp'] = td[2].get_text().strip()
    curr_item['trade'] = td[8].get_text().strip()
    top_twenty_by_trade.append(curr_item)

del(top_twenty_by_trade[0])
with open('marketmovers/top_twenty_by_trade.txt', 'w') as f:
    f.write(json.dumps(top_twenty_by_trade))