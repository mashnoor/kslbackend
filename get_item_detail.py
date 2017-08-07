import requests, grequests

from bs4 import BeautifulSoup

item_detail_urls = ["http://www.cse.com.bd/companyDetails.php?scriptCode=QUJCQU5L"]

req = (grequests.get(url) for url in item_detail_urls)

response = grequests.map(req)

print response