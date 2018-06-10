import requests
from bs4 import BeautifulSoup
import json

url = "http://www.cse.com.bd/"

r = requests.get(url)

soup = BeautifulSoup(r.content, 'lxml')

############## INDEXES ##############
div_attrs = {"class":"indexvalue"}
index_divs = soup.find_all("div", div_attrs)

all_idexes = {}
#CSE50
cse50_values = {}
cse50_div = index_divs[0]
inner_divs = cse50_div.find_all('div')
cse50_values['cse50value'] = inner_divs[1].get_text().strip()
cse50_values['cse50change'] = inner_divs[2].get_text().strip()
all_idexes.update(cse50_values)


#CSE30
cse30_values = {}
cse30_div = index_divs[1]
inner_divs = cse30_div.find_all('div')
cse30_values['cse30value'] = inner_divs[1].get_text().strip()
cse30_values['cse30change'] = inner_divs[2].get_text().strip()
all_idexes.update(cse30_values)

#CSCX
cscx_values = {}
cscx_div = index_divs[2]
inner_divs = cscx_div.find_all('div')
cscx_values['cscxvalue'] = inner_divs[1].get_text().strip()
cscx_values['cscxchange'] = inner_divs[2].get_text().strip()
all_idexes.update(cscx_values)

#CSE50
caspi_values = {}
caspi_div = index_divs[3]
inner_divs = caspi_div.find_all('div')
caspi_values['caspivalue'] = inner_divs[1].get_text().strip()
caspi_values['caspichange'] = inner_divs[2].get_text().strip()
all_idexes.update(caspi_values)

#CSI
csi_values = {}
csi_div = index_divs[4]
inner_divs = csi_div.find_all('div')
csi_values['csivalue'] = inner_divs[1].get_text().strip()
csi_values['csichange'] = inner_divs[2].get_text().strip()
all_idexes.update(csi_values)




########### GET Market Summary ##############
market_summary_div_attrs = {"class":"ColNumUpdate"}
market_summary_divs = soup.find_all("div", market_summary_div_attrs)
skipped_the_first_row = False
market_summary_field_names = ["value_in_taka", "volume", "contract_number", "issues_traded", "issues_advanced", "issues_declined", "issues_unchanged", "issued_capital", "closing_market_capitalization"]
market_summary_values = []

for value_div in market_summary_divs:
    market_summary_values.append(value_div.get_text().strip())


market_summary_values = dict(zip(market_summary_field_names, market_summary_values))



## Write The Index Values
with open("homedatas/all_indexes.txt", "w") as f:
    f.write(json.dumps(all_idexes))

## Write The Market Summary Values
with open('homedatas/market_summary.txt', "w") as f:
    f.write(json.dumps(market_summary_values))


