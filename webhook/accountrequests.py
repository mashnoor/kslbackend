from flask import Blueprint, render_template, request
import dbhelper

account_request_api = Blueprint('requisitions_api', __name__)





@account_request_api.route("/accountrequests")
def accountrequests():
    #print dbhelper.getAccounts()
    return render_template("accountrequests.html", accounts=dbhelper.getAccounts())


@account_request_api.route("/requestaccount", methods=["POST"])
def requestaccount():
    req_json = request.get_json()
    acc = dbhelper.Account()
    acc.email = req_json['email']
    acc.mobile = req_json['mobile']
    acc.password = req_json['username']
    acc.username = req_json['password']
    acc.isApproved = 0
    dbhelper.saveAccount(acc)
    return "Request for account creation in successful"