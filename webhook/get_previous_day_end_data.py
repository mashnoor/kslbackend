from flask import Blueprint, render_template, request, redirect, url_for
import json

account_request_api = Blueprint('previous_day_end_data', __name__)
import requests
from bs4 import BeautifulSoup


@previous_day_end_data.route('/getdayenddata', methods=['POST'])
def getJsonofDayEnd(fromYear, fromMonth, fromDay, toYear, toMonth, toDay, company):
    fromYear = request.form.get('fromyear')
    fromMonth = request.form.get('frommonth')
    fromDay = request.form.get('fromday')
    toYear = request.form.get('toyear')
    toMonth = request.form.get('tomonth')
    toDay = request.form.get('todays')
    company = request.form.get('company')
    day_end_archive_url = "http://www.dse.com.bd/day_end_archive.php"
    attrs = {"DayEndSumDate1": fromYear + "-" + fromMonth + "-" + fromDay,
             "DayEndSumDate1_dp": "1",
             "DayEndSumDate1_year_start": "2016",
             "DayEndSumDate1_year_end": "2018",
             "DayEndSumDate1_da1": "",
             "DayEndSumDate1_da2": "",
             "DayEndSumDate1_sna": "1",
             "DayEndSumDate1_aut": "",
             "DayEndSumDate1_frm": "",
             "DayEndSumDate1_tar": "",
             "DayEndSumDate1_inp": "1",
             "DayEndSumDate1_fmt": "j F Y",
             "DayEndSumDate1_dis": "",
             "DayEndSumDate1_pr1": "",
             "DayEndSumDate1_pr2": "",
             "DayEndSumDate1_prv": "",
             "DayEndSumDate1_pth": "calendar/",
             "DayEndSumDate1_spd": "[[],[],[]]",
             "DayEndSumDate1_spt": "0",
             "DayEndSumDate1_och": "",
             "DayEndSumDate1_str": "0",
             "DayEndSumDate1_rtl": "",
             "DayEndSumDate1_wks": "",
             "DayEndSumDate1_int": "1",
             "DayEndSumDate1_hid": "1",
             "DayEndSumDate1_hdt": "1000",
             "DayEndSumDate1_day": fromDay,
             "DayEndSumDate1_month": fromMonth,
             "DayEndSumDate1_year": fromYear,
             "DayEndSumDate2": toYear + "-" + toMonth + "-" + toDay,
             "DayEndSumDate2_dp": "1",
             "DayEndSumDate2_year_start": "2016",
             "DayEndSumDate2_year_end": "2018",
             "DayEndSumDate2_da1": "",
             "DayEndSumDate2_da2": "",
             "DayEndSumDate2_sna": "1",
             "DayEndSumDate2_aut": "",
             "DayEndSumDate2_frm": "",
             "DayEndSumDate2_tar": "",
             "DayEndSumDate2_inp": "1",
             "DayEndSumDate2_fmt": "j F Y",
             "DayEndSumDate2_dis": "",
             "DayEndSumDate2_pr1": "",
             "DayEndSumDate2_pr2": "",
             "DayEndSumDate2_prv": "",
             "DayEndSumDate2_pth": "calendar/",
             "DayEndSumDate2_spd": "[[],[],[]]",
             "DayEndSumDate2_spt": "0",
             "DayEndSumDate2_och": "",
             "DayEndSumDate2_str": "0",
             "DayEndSumDate2_rtl": "",
             "DayEndSumDate2_wks": "",
             "DayEndSumDate2_int": "1",
             "DayEndSumDate2_hid": "1",
             "DayEndSumDate2_hdt": "1000",
             "DayEndSumDate2_day": toDay,
             "DayEndSumDate2_month": toMonth,
             "DayEndSumDate2_year": toYear,
             "Symbol": company,
             "ViewDayEndArchive": "View Day End Archive"}
    r = requests.post(day_end_archive_url, attrs)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table",
                      attrs={"border": "0", "bgcolor": "#808000", "cellspacing": "1"})

    data = []
    for tr in table.find_all("tr"):
        curr_data = {}
        tds = tr.find_all("td")
        curr_data["date"] = str(tds[1].text)
        curr_data["volume"] = str(tds[11].text).replace(",", "")
        data.append(curr_data)
    del data[0]
    return json.dumps(data)



