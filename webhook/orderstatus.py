import requests
from bs4 import BeautifulSoup

url = "https://bangladeshstockmarket.com/LoadBalance.do"

statusUrl = "https://bangladeshstockmarket.com/TradeBookView.do"

verifyPassword = "https://bangladeshstockmarket.com/ViewOrder.do"


def status(loginid, password, startdate, enddate):
    d = {"page": "3",
         "startdate": startdate,
         "enddate": enddate,
         "selectStatus": "ALL",
         "selectSegement": "DELIVERY",
         "stockCode": "",
         "selectExchange": "CTG",
         "boardType": "AL",
         "newSubmit": "Y",
         "orderno": "",
         "exchrefno": "",
         "orderrefno": "",
         "process": "",
         "hidexchange": "",
         "hidsymbol": "",
         "hidbuysell": "",
         "hidquantity": "0",
         "hidprice": "0.0",
         "show": "",
         "lastModifiedDate": "0",
         "lastModifiedTime": "0",
         "pendingqty": "0",
         "hidreferenceid": "",
         "hidboardtype": "",
         "hidminfill": "0",
         "hiddisquan": "0",
         "hidordertype": "",
         "hidtriprice": "0.0",
         "hidfilltype": "",
         "selectProduct": "EQUITES",
         "hidexpirydate": "0"}
    login_data = {'loginid': loginid, 'password': password, 'lang1': 'default'}

    with requests.Session() as s:
        r = s.post(url, data=login_data)
        # print r.text
        r = s.post(verifyPassword, data={'pagePassword': password})
        if (r.text == "NOTOK"):
            return "Login Failed"
        r = s.post(statusUrl, data=d)
        print(r.text)
        return r.text
