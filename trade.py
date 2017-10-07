import requests
from bs4 import BeautifulSoup

url = "https://bangladeshstockmarket.com/LoadBalance.do"


order1url = "https://bangladeshstockmarket.com/Order1.do?exchangeSelected=CTG"


verifyPassword = "https://bangladeshstockmarket.com/PasswordCheck.do"
def buy_item(loginid, password, symbol, qty, price):
    d = {'loginid':loginid, 'password':password, 'lang1':'default'}
    order1_data = {'spdBuySymbol':'', 'spdSellSymbol':'','submitbutton':'Submit', 'exchange':'CTG',
    'selectProduct':'EQUITY', 'segment':'DELIVERY', 'symbol':symbol,'buysell':'BUY',
    'quantity':qty, 'referenceId':'','pricetype':'LIMIT','price':price, 'triprice':'0',
    'disquan':'', 'protectionPercent':'', 'filltype':'GFD','minFillQty':'',
    'expirydate':'','settlerid':'','priceViolation':'N','lotsize':'1', 'userExchangeList':'CTG',
    'hidboardtype':'NR'}   
    
    with requests.Session() as s:
        r = s.post(url, data=d)
        #print r.text
        r = s.post(verifyPassword, data={'pagePassword':password})
        if(r.text == "NOTOK"):
            return "Login Failed"
        r = s.post(order1url, data=order1_data)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup.find_all('font')[0].text
        #with open('data.txt', 'w+') as f:
        #   f.write(r.text)

