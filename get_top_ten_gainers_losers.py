from bs4 import BeautifulSoup
import requests
import json
from flask import Blueprint

url = "https://www.cse.com.bd"

########## TOP GAINERS ##########

r = requests.get(url, verify=False)
soup = BeautifulSoup(r.content, "html.parser")

divs = soup.find_all('div', {'class': 'tap_content'})

top_gainer_div = divs[0]
top_gainers = []
for item in top_gainer_div.find_all('div', {'class': 'MIrow1'}):
    curr_gainer = {}
    inner_divs = item.find_all('div')

    curr_gainer["item"] = inner_divs[0].text
    curr_gainer["ltp"] = inner_divs[1].text
    curr_gainer["changeval"] = inner_divs[2].text
    curr_gainer["changepercentage"] = inner_divs[3].text
    top_gainers.append(curr_gainer)
print(top_gainers)
with(open('gainer_loser/gainers.txt', 'w')) as f:
    f.write(json.dumps(top_gainers))

############ TOP LOSERS ##############


top_losers_div = divs[1]
top_losers = []
for item in top_losers_div.find_all('div', {'class': 'MIrow1'}):
    curr_loser = {}
    inner_divs = item.find_all('div')
    curr_loser["item"] = inner_divs[0].text
    curr_loser["ltp"] = inner_divs[1].text
    curr_loser["changeval"] = inner_divs[2].text
    curr_loser["changepercentage"] = inner_divs[3].text
    top_losers.append(curr_loser)

print(top_losers)
with(open('gainer_loser/losers.txt', 'w')) as f:
    f.write(json.dumps(top_losers))
