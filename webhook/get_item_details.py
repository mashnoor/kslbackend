#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup

from flask import Blueprint

import json, requests

get_item_detail_api = Blueprint('get_item_details_api', __name__)


def get_url(item_name):
    base_url = "http://www.dsebd.org/displayCompany.php?name="
    return base_url + item_name


@get_item_detail_api.route("/getitemdetail/<item_name>")
def getItemDetail(item_name):
    final_result = {}

    r = requests.get(get_url(item_name))

    soup = BeautifulSoup(str(r.text).encode('ascii', 'ignore').decode('ascii'), "html.parser")

    ################## GRAB COMPANY NAME #####################
    comp_table = soup.find("th", {"style": "text-align:center !important;"})
    company_name = comp_table.get_text().replace("Company Name: ", '').strip()
    print(company_name)

    ####################   Grab Data from Market Information    #########################
    table_params = {'border': '1', 'cellspacing': '1', 'width': '100%'}
    market_info_tables = soup.find_all("table", table_params)
    ###################    First Table ####################################
    # m_i_table_params ={'width':"100%", 'border':'0', 'cellpadding':'0', 'cellspacing':'1', 'bgcolor':'#C0C0C0'}
    m_i_table = market_info_tables[0]
    values = []
    for td in m_i_table.find_all("tr"):
        values.append(td.text)
        # print td.text

    lastTrade = str(values[3]).replace("Last Trading Price", "").strip()
    print("Last Tarade - " + lastTrade)

    change_num = str(values[5]).strip()
    change_num = change_num[:-7].replace("Change*", "").strip()

    print("Change Num: " + change_num)
    change_percentage = str(values[5]).replace(change_num, "").replace("Change*", "").strip()
    print("Change Percentage:" + change_percentage)
    open_price = str(values[8]).replace("Opening Price", "").strip()
    print("Open Price: " + open_price)

    adjust_open_price = str(values[9]).replace("Adjusted Opening Price", "").strip()
    print("Adjust Opening Price: " + adjust_open_price)
    yesterday_close_price = str(values[10]).replace("Yesterday's Closing Price", "").strip()
    print("YCP:" + yesterday_close_price)
    closePrice = str(values[11]).replace("Closing Price", "").strip()
    print("Closing Price: " + closePrice)
    daysRange = str(values[12]).replace("Day's Range", "").strip()
    print("Days Range: " + daysRange)

    value = str(values[13]).replace("Day's Value (mn)", "").strip()
    print(value)
    weekRange = str(values[14]).replace("52 Weeks' Moving Range", "").strip()
    print("Week's Range: " + weekRange)
    volume = str(values[15]).replace("Day's Volume (Nos.)", "").strip()
    print("Volume : " + volume)
    totalTrade = str(values[16]).replace("Day's Trade (Nos.)", "").strip()
    print("Total Trade: " + totalTrade)
    market_capital = str(values[17]).replace("Market Capitalization (mn)", '').strip()
    print("Market Capital: " + market_capital)

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


    authorized_capital = basic_info_table[3].replace("Authorized Capital (mn)", "").strip()
    print("Authorized Capital: " + authorized_capital)
    paidupvalue = basic_info_table[4].replace("Paid-up Capital (mn)", "").strip()
    print("Paid Up Value: " + paidupvalue)

    facevalue = basic_info_table[5].replace("Face/par Value", "").strip()
    print("Face Value: " + facevalue)
    marketLot = basic_info_table[9].replace("Market Lot", "").strip()
    print("Market Lot: " + marketLot)

    noofsecurities = basic_info_table[6].replace("Total No. of Outstanding Securities", "").strip()
    print("Total no of sec. : " + noofsecurities)
    segment = basic_info_table[10].replace("Sector", "").strip()
    print("Segment: " + segment)

    ############### END OF BASIC INFORMATION ############




    ################ P/E Ratio ######################

    # Un-Audited
    peratio_table = market_info_tables[4]

    values = []

    for row in peratio_table.find_all("tr"):
        cells = row.find_all("td")
        for cell in cells:
            values.append(cell.get_text().strip())
    peratio_basic = "UA: " + values[15]
    print(peratio_basic)
    peratio_diluted = "UA: " + values[22]
    print(peratio_diluted)

    # Audited
    peratio_table = market_info_tables[5]

    values = []

    for row in peratio_table.find_all("tr"):
        cells = row.find_all("td")
        for cell in cells:
            values.append(cell.get_text().strip())
    peratio_basic_a = " A: " + values[15]
    print("PE A: " + peratio_basic_a)
    peratio_diluted_a = " A: " + values[22]

    print("PED A: " + peratio_diluted_a)
    peratio_basic = peratio_basic + peratio_basic_a
    peratio_diluted = peratio_diluted + peratio_diluted_a

    '''
    ############################ FINANCIAL PERFORMANCE ##########################
    table_params = {'border': "1", 'width': "100%", 'cellspacing': "0", 'cellpadding': "0"}
    
    fp_table = soup.find_all("table", table_params)[1]
    values = []
    for row in fp_table.find_all("tr"):
        cells = row.find_all("td")
        for cell in cells:
            values.append(cell.get_text().strip())
    
        # 2013 Year index - 131
    eps_2013 = values[132]
    netassetvalue_2013 = values[136]
    
    netprofit_continue_2013 = values[138]
    
    netprofit_extraordinary_2013 = values[139]
    # 2014 Year Index - 140
    
    eps_2014 = values[141]
    netassetvalue_2014 = values[145]
    netprofit_continue_2014 = values[147]
    netprofit_extraordinary_2014 = values[148]
    
    ######## DIVIDEND ##############
    table_params = {'border': "1", 'width': "100%", 'cellspacing': "0", 'cellpadding': "0"}
    
    dividend_table = soup.find_all("table", table_params)[2]
    values = []
    for row in dividend_table.find_all("tr"):
        cells = row.find_all("td")
        for cell in cells:
            values.append(cell.get_text().strip())
    
    dividend_2014 = values[80]
    dividend_2013 = values[75]
    dividend_2012 = values[70]
    dividend_2011 = values[65]
    dividend_2010 = values[60]
    dividend_2009 = values[55]
    '''
    #################### HISTORY AND OTHERS #########################


    history_table = market_info_tables[2]

    values = []
    for row in history_table.find_all("tr"):
        cells = row.find_all("td")
        for cell in cells:
            values.append(cell.get_text().strip())

    lastAgm = values[0].replace("Last AGM held on:", "").replace("For the year ended:", "")[:-13].strip()
    print("Last AGM: " + lastAgm)

    yearEnd = values[9].strip()
    print("Year End: " + yearEnd)

    bonusIssue = values[5].strip()
    print("Bonus Issue: " + bonusIssue)
    rightIssue = values[7].strip()
    print("Right Issue: " + rightIssue)
    reserveandsurplus = values[11]
    print("Reserve and surplus: " + reserveandsurplus)

    ################## SHARE PERCENTAGE ####################


    sp_table = market_info_tables[8]

    values = []
    for row in sp_table.find_all("tr"):
        cells = row.find_all("td")
        for cell in cells:
            values.append(cell.get_text().strip())

    marketCatagory = values[5]
    print("Market Catagory: " + marketCatagory)
    sponsor = values[10].replace("Sponsor/Director:", "").strip()
    print("Sponsor: " + sponsor)
    govt = values[11].replace("Govt:", '').strip()
    print("Govt. : " + govt)
    institute = values[12].replace("Institute:", '').strip()
    print("Institute: " + institute)
    foreign = values[13].replace("Foreign:", '').strip()
    print("Foreign: " + foreign)

    public = values[14].replace("Public:", "").strip()
    print("Public: " + public)

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
    final_result["value(mn)"] = value
    final_result["item"] = item_name

    json_converted = json.dumps(final_result)
    return json_converted
