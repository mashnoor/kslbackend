from bs4 import BeautifulSoup
import json
import requests

url = "https://www.cse.com.bd"

r = requests.get(url, verify=False)

soup = BeautifulSoup(r.content, 'html5lib')

############## INDEXES ##############
div_attrs = {"id": "mitabs-1"}
inner_div_attrs = {"class": "top_Col3"}
index_divs = soup.find_all("div", div_attrs)

all_idexes = {}
# CSE50
cse50_values = {}
cse50_div = index_divs[4]
inner_divs = cse50_div.find_all('div', inner_div_attrs)
cse50_values['cse50value'] = inner_divs[0].get_text().strip()
cse50_values['cse50change'] = inner_divs[1].get_text().strip()
all_idexes.update(cse50_values)

# CSE30
cse30_values = {}
cse30_div = index_divs[5]
inner_divs = cse30_div.find_all('div', inner_div_attrs)
cse30_values['cse30value'] = inner_divs[0].get_text().strip()
cse30_values['cse30change'] = inner_divs[1].get_text().strip()
all_idexes.update(cse30_values)

# CSCX
cscx_values = {}
cscx_div = index_divs[6]
inner_divs = cscx_div.find_all('div', inner_div_attrs)
cscx_values['cscxvalue'] = inner_divs[0].get_text().strip()
cscx_values['cscxchange'] = inner_divs[1].get_text().strip()
all_idexes.update(cscx_values)

# CSE50
caspi_values = {}
caspi_div = index_divs[7]
inner_divs = caspi_div.find_all('div', inner_div_attrs)
caspi_values['caspivalue'] = inner_divs[0].get_text().strip()
caspi_values['caspichange'] = inner_divs[1].get_text().strip()
all_idexes.update(caspi_values)

# CSI
csi_values = {}
csi_div = index_divs[8]
inner_divs = csi_div.find_all('div', inner_div_attrs)
csi_values['csivalue'] = inner_divs[0].get_text().strip()
csi_values['csichange'] = inner_divs[1].get_text().strip()
all_idexes.update(csi_values)
print(all_idexes)
########### GET Market Summary ##############
market_summary_div_attrs = {"class": "value1"}
market_summary_divs = soup.find_all("div", market_summary_div_attrs)
skipped_the_first_row = False
market_summary_field_names = ["issues_traded", "volume", "issued_capital", "value_in_taka", "contract_number",
                              "closing_market_capitalization"] #, "issues_advanced", "issues_declined", "issues_unchanged"
market_summary_values = []

for value_div in market_summary_divs:
    market_summary_values.append(str(value_div.get_text()).split(' ')[0].strip())

market_summary_values = dict(zip(market_summary_field_names, market_summary_values))

print(market_summary_values)

## Write The Index Values
with open("homedatas/all_indexes.txt", "w") as f:
    f.write(json.dumps(all_idexes))

## Write The Market Summary Values
with open('homedatas/market_summary.txt', "w") as f:
    f.write(json.dumps(market_summary_values))
