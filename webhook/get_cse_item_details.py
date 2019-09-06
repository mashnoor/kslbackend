#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup

from flask import Blueprint

import json

import settings

if settings.use_fast_requests:
    import faster_than_requests as req
else:
    import requests

get_cse_item_detail_api = Blueprint('get_cse_item_details_api', __name__)


def get_url(item_name):
    base_url = "https://www.cse.com.bd/company/companydetails/"
    return base_url + item_name

@get_cse_item_detail_api.route('/getitemdetail/cse/<item_name>')
def getItemDetail(item_name):
    final_result = {}
    url = get_url(item_name)

    if settings.use_fast_requests:
        html = req.get2str(url)
    else:
        r = requests.get(url, verify=False)
        html = r.text

    soup = BeautifulSoup(str(html).encode('ascii', 'ignore').decode('ascii'), "html.parser")

    ################## GRAB COMPANY NAME #####################
    comp_table = soup.find("div", {"class": "com_title"})
    company_name = comp_table.get_text().strip()
    print(company_name)

    ####################   Grab Data from Market Information    #########################
    table_params = {'border': '0', 'cellspacing': '0', 'width': '100%', 'cellpadding': '0'}
    market_info_tables = soup.find_all("table", table_params)

    ###################    First Table ####################################
    m_i_table = market_info_tables[1]

    values = []
    for tr in m_i_table.find_all("tr"):
        td = tr.find_all("td")
        values.append(str(td[1].text).strip())
        # print td.text

    lastTrade = values[0]
    print("Last Tarade - " + lastTrade)

    change_percentage = values[2]
    print("Change Percentage:" + change_percentage)
    open_price = values[3]
    print("Open Price: " + open_price)

    change_num = "0"
    try:
        change_num = str(format(float(lastTrade) - float(open_price), '.2f'))
    except:
        pass

    print("Change Num: " + change_num)

    daysRange = values[4]
    print("Days Range: " + daysRange)

    ############### Second Table ##################
    m_i_table = market_info_tables[2]
    values = []
    for tr in m_i_table.find_all("tr"):
        td = tr.find_all("td")
        values.append(str(td[1].text).strip())
        # print td.text

    totalTrade = values[0]
    print("Total Trade: " + totalTrade)

    volume = values[1]
    print("Volume : " + volume)

    closePrice = values[2]
    print("Closing Price: " + closePrice)

    yesterday_close_price = values[3]
    print("YCP:" + yesterday_close_price)

    market_capital = values[4]
    print("Market Capital: " + market_capital)

    ############## BASIC INFO ############
    m_i_table = market_info_tables[4]
    values = []
    for tr in m_i_table.find_all("tr"):
        td = tr.find_all("td")
        try:
            values.append(str(td[1].text).strip())
        except:
            pass

    marketLot = values[2]
    print("Market Lot: " + marketLot)

    facevalue = values[3]
    print("Face Value: " + facevalue)

    paidupvalue = values[4]
    print("Paid Up Value: " + paidupvalue)

    #### SECOND TABLE ######
    m_i_table = market_info_tables[5]
    values = []
    for tr in m_i_table.find_all("tr"):
        td = tr.find_all("td")
        try:
            values.append(str(td[1].text).strip())
        except:
            pass

    marketCatagory = values[3]
    print("Market Catagory: " + marketCatagory)

    authorized_capital = values[4]
    print("Authorized Capital: " + authorized_capital)

    noofsecurities = values[5]
    print("Total no of sec. : " + noofsecurities)

    weekRange = values[6]
    print("Week's Range: " + weekRange)

    yearEnd = values[7]
    print("Year End: " + yearEnd)

    reserveandsurplus = values[8]
    print("Reserve and surplus: " + reserveandsurplus)

    ######## SHARE PERCENTAGE
    m_i_table = market_info_tables[7]
    values = []
    td = m_i_table.find_all("tr")[1]

    for td in td.find_all('td'):
        try:
            values.append(str(td.text).strip())
        except:
            pass

    sponsor = values[1]
    print("Sponsor: " + sponsor)

    govt = values[2]
    print("Govt. : " + govt)

    institute = values[3]
    print("Institute: " + institute)

    foreign = values[4]
    print("Foreign: " + foreign)

    public = values[5]
    print("Public: " + public)

    #### LAST AGM ####
    lastAgmTexTd = soup.find("td", text="AGM Date ")
    lastAgmDateTd = lastAgmTexTd.find_next_sibling("td")


    values = []
    values.append(str(lastAgmDateTd.text).strip())

    lastAgm = values[0]
    print("Last AGM: " + lastAgm)

    #### Bonous Issue ####
    bonousIssueTextTd = soup.find("td", text="Bonus Issue ")
    bonousIssueTd = bonousIssueTextTd.find_next_sibling("td")
    values = []
    values.append(str(bonousIssueTd.text).strip())

    bonusIssue = values[0]
    print("Bonus Issue: " + bonusIssue)

    #########      WE ARE DONE WITH MARKET INFO TABLE #####################

    ################## BASIC INFORMATION ########################
    second_table = market_info_tables[1]

    basic_info_table = []
    try:

        for td in second_table.find_all("tr"):
            basic_info_table.append(td.text)
    except:
        pass
    # print str(values_second_table[2])

    ############### END OF BASIC INFORMATION ############

    ####Un Supported
    rightIssue = "--"
    peratio_basic = "--"
    peratio_diluted = "--"
    amount_traded_in_bdt = "--"
    adjust_open_price = "--"
    segment = "--"

    ####### GATHER ALL AND ADDEM TOGETHER
    final_result["closeprice"] = closePrice
    final_result["ycp"] = yesterday_close_price
    final_result["openprice"] = open_price
    final_result["adjustopenprice"] = adjust_open_price
    final_result["daysrange"] = daysRange
    final_result["volume"] = volume
    final_result["totaltrade"] = totalTrade
    final_result["marketcapital"] = market_capital
    final_result["authorizedcapital"] = authorized_capital  # authorized_capital
    final_result["paidupvalue"] = paidupvalue  # paidupvalue
    final_result["facevalue"] = facevalue  # facevalue
    final_result["noofsecurities"] = noofsecurities  # noofsecurities
    final_result["weekrange"] = weekRange  # weekRange
    final_result["marketlot"] = marketLot  # marketLot
    final_result["segment"] = segment  # segment
    final_result["rightissue"] = rightIssue  # rightIssue
    final_result["yearend"] = yearEnd  # yearEnd
    final_result["reserveandsurplus"] = reserveandsurplus  # reserveandsurplus
    final_result["bonousissue"] = bonusIssue  # bonusIssue
    final_result["companyname"] = company_name
    final_result["ltp"] = lastTrade
    final_result["changeval"] = change_num
    final_result["changepercentage"] = change_percentage
    final_result["lastagm"] = lastAgm  # lastAgm
    final_result["p_e_ratio_basic"] = peratio_basic  # peratio_basic
    final_result["p_e_ratio_diluted"] = peratio_diluted  # peratio_diluted
    final_result["marketcatagory"] = marketCatagory  # marketCatagory
    final_result["fp2013_epscontinueoperation"] = "0"  # eps_2013
    final_result["fp2013_NAV"] = "0"  # netassetvalue_2013
    final_result["fp2013_NPATcontinueoperation"] = "0"  # netprofit_continue_2013
    final_result["fp2013_NPATextraordinaryincome"] = "0"  # netprofit_extraordinary_2013
    final_result["fp2014_epscontinueoperation"] = "0"  # eps_2014
    final_result["fp2014_NAV"] = "0"  # netassetvalue_2014
    final_result["fp2014_NPATextraordinaryincome"] = "0"  # netprofit_extraordinary_2014
    final_result["fp2014_NPATcontinueoperation"] = "0"  # netprofit_continue_2014
    final_result["fpcontinue_dividend_2009"] = "0"  # dividend_2009
    final_result["fpcontinue_dividend_2010"] = "0"  # dividend_2010
    final_result["fpcontinue_dividend_2011"] = "0"  # dividend_2011
    final_result["fpcontinue_dividend_2012"] = "0"  # dividend_2012
    final_result["fpcontinue_dividend_2013"] = "0"  # dividend_2013
    final_result["fpcontinue_dividend_2014"] = "0"  # dividend_2014
    final_result["sp_sponsor_director"] = sponsor  # sponsor
    final_result["sp_govt"] = govt  # govt
    final_result["sp_institute"] = institute  # institute
    final_result["sp_foreign"] = foreign  # foreign
    final_result["sp_public"] = public  # public
    final_result["amounttradedinbdt"] = amount_traded_in_bdt
    final_result["item"] = item_name

    json_converted = json.dumps(final_result)
    return json_converted
