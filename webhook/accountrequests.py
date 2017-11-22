from flask import Blueprint, render_template, request, redirect, url_for
import dbhelper
import json
account_request_api = Blueprint('account_request_api', __name__)


@account_request_api.route("/accountrequests")
def accountrequests():
    # print dbhelper.getAccounts()
    return render_template("accountrequests.html", accountrequests=dbhelper.getAccountRequests())


@account_request_api.route("/requestaccount", methods=["POST"])
def requestaccount():
    req_json = request.get_json()
    acc = dbhelper.AccountRequest()
    acc.email = req_json['email']
    acc.mobile = req_json['mobile']
    acc.password = req_json['username']
    acc.username = req_json['password']
    acc.isApproved = 0
    dbhelper.save(acc)
    return "Request for account creation in successful"


@account_request_api.route("/accounts")
def accounts():
    return render_template("accounts.html", accounts=dbhelper.getAccounts())



@account_request_api.route("/addaccount", methods=["POST"])
def addaccount():
    acc = dbhelper.Account()
    acc.name = request.form.get("accountname")
    acc.detail = request.form.get("accountdetail")
    acc.masterId = request.form.get("masterid")
    acc.masterPassword = request.form.get("masterpassword")
    dbhelper.save(acc)
    return accounts()

@account_request_api.route("/<masterid>/itsaccounts/")
def itsaccounts(masterid):
    return render_template("itsaccounts.html", masterid=masterid, itsaccounts=dbhelper.getItsAccounts(masterid))

@account_request_api.route("/itsaccounts", methods=["POST"])
def getItsAccounts():
    r = request.get_json()
    masterid = r['masterid']
    masterpass = r['masterpass']
    itsaccounts = dbhelper.getItsAccountsMobile(masterid, masterpass)
    allitsaccounts = []
    for itsaccount in itsaccounts:
        data = {
            "itsaccountno" : itsaccount.itsNo,
            "itsaccountpass": itsaccount.password
        }
        allitsaccounts.append(data)
    return json.dumps(allitsaccounts)

@account_request_api.route("/<masterid>/additsaccount", methods=["POST"])
def additsaccount(masterid):
    itsacc = dbhelper.ITSAccount()
    itsacc.itsNo = request.form.get("itsaccountno")
    itsacc.password = request.form.get("itspassword")
    dbhelper.addItsAccoount(masterid, itsacc)
    return itsaccounts(masterid)

@account_request_api.route("/<masterid>/additsaccountmobile", methods=["POST"])
def additsaccountmobile(masterid):
    itsacc = dbhelper.ITSAccount()
    r = request.get_json()
    itsacc.itsNo = r["itsaccountno"]
    itsacc.password = r["itsaccountpass"]
    dbhelper.addItsAccoount(masterid, itsacc)
    return "success"

@account_request_api.route("/masterlogin", methods=["POST"])
def master_login():
    r = request.get_json()
    masterid = r['masterid']
    masterpass = r['masterpass']
    if dbhelper.isValiedMasterId(masterid, masterpass):
        return "success"
    else:
        return "failed"

@account_request_api.route("/<masterid>/clientids/")
def clientids(masterid):
    return render_template("clientids.html", masterid=masterid, clientids=dbhelper.getClientIds(masterid))

@account_request_api.route("/<masterid>/addclientid", methods=["POST"])
def addclientid(masterid):
    client = dbhelper.Clientid()
    client.clientidno = request.form.get("clientid")

    dbhelper.addClientId(masterid, client)
    return clientids(masterid)

@account_request_api.route("/clientids", methods=["POST"])
def getClientIDsMobile():
    r = request.get_json()

    masterid = r['masterid']
    masterpass = r['masterpass']
    clientIds = dbhelper.getClientIdsMobile(masterid, masterpass)
    ids = []
    for id in clientIds:
        ids.append(id.clientidno)
  

    return json.dumps(ids)