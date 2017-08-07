import requests
from bs4 import BeautifulSoup
import json

items_list_url = "http://www.cse.com.bd/company_info_url.php"
company_detail_link_prefix = "http://www.cse.com.bd/"

r = requests.get(items_list_url)

soup = BeautifulSoup(r.content, 'lxml')
table_attrs = {"id":"report", "width":"100%", "border":"0", "cellpadding":"0", "cellspacing":"0", "bgcolor":"#355DA2"}

table = soup.find("table", table_attrs)
all_company = []  # Storing all the scd, company name and link of all company in this array
i = 0
for tr in table.find_all("tr"):
   try:
       td = tr.find_all('td')
       current_company = {}
       current_company['scd'] = str(td[2].text)
       current_company['name'] = str(td[3].text)
       current_company['link'] = str(company_detail_link_prefix + td[4].find('a')['href'])
       all_company.append(current_company)
   except:
       pass

json_converted = json.dumps(all_company)
with open('all_company_info.txt', 'wb') as f:
    f.write(json_converted)

