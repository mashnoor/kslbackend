import requests, grequests

from bs4 import BeautifulSoup
from helpers import get_column_values

item_detail_urls = ["http://www.cse.com.bd/companyDetails.php?scriptCode=QUJCQU5L"]

req = (grequests.get(url) for url in item_detail_urls)

responses = grequests.map(req)


soup = BeautifulSoup(responses[0].content, 'lxml')
table_attrs = {"width":"100%", "border":"0", "cellpadding":"0", "cellspacing":"0"}
table = soup.find_all("table", table_attrs)

current_item_info = {}  # Store all the info of the company

############# Parse Current Market Info Table ############

inner_tables = table[2].find_all("table")
get_column_values(str(inner_tables[0]), ['ltp', 'ltd', 'change', 'openprice', 'range'])
get_column_values(str(inner_tables[1]), ['trade', 'volume', 'closeprice', 'ycp', 'capital'])


############ Parse Contract Info and Basic Info ##############

print get_column_values(str(table[5]), [1,2,3,4,5,6,7,8, 9,10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
