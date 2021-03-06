from flask import Blueprint, render_template, request, redirect, url_for
import dbhelper
import json
import flask_login

account_request_api = Blueprint('account_request_api', __name__)


@account_request_api.route("/accountrequests")
@flask_login.login_required
def accountrequests():
    # print dbhelper.getAccounts()
    manager = dbhelper.DBManager()
    return render_template("accountrequests.html", accountrequests=manager.getAccountRequests())


@account_request_api.route("/requestaccount", methods=["POST"])
def requestaccount():
    acc = dbhelper.AccountRequest()
    acc.email = request.form.get("email")
    acc.mobile = request.form.get("phone")
    acc.password = ""
    acc.name = request.form.get("accname")
    acc.details = request.form.get("details")
    manager = dbhelper.DBManager()
    manager.save(acc)
    return "Request for account creation in successful"


@account_request_api.route("/accounts")
@flask_login.login_required
def accounts():
    manager = dbhelper.DBManager()
    return render_template("accounts.html", accounts=manager.getAccounts())


@account_request_api.route("/addaccount", methods=["POST"])
def addaccount():
    acc = dbhelper.Account()
    acc.name = request.form.get("accountname")
    acc.detail = request.form.get("accountdetail")
    acc.masterId = request.form.get("masterid")
    acc.email = request.form.get("email")
    acc.masterPassword = request.form.get("masterpassword")
    manager = dbhelper.DBManager()
    manager.save(acc)
    return redirect(url_for('account_request_api.accounts'))


@account_request_api.route("/<masterid>/itsaccounts/")
@flask_login.login_required
def itsaccounts(masterid):
    manager = dbhelper.DBManager()
    return render_template("itsaccounts.html", masterid=masterid, itsaccounts=manager.getItsAccounts(masterid))


@account_request_api.route("/itsaccounts", methods=["POST"])
def getItsAccounts():
    manager = dbhelper.DBManager()
    masterid = request.form.get('masterid')
    masterpass = request.form.get('masterpass')
    itsaccounts = manager.getItsAccountsMobile(masterid, masterpass)
    allitsaccounts = []
    for itsaccount in itsaccounts:
        data = {
            "itsaccountno": itsaccount.itsNo,
            "itsaccountpass": itsaccount.password
        }
        allitsaccounts.append(data)
    return json.dumps(allitsaccounts)


@account_request_api.route("/<masterid>/additsaccount", methods=["POST"])
def additsaccount(masterid):

    itsacc = dbhelper.ITSAccount()
    itsacc.itsNo = request.form.get("itsaccountno")
    itsacc.password = request.form.get("itspassword")
    manager = dbhelper.DBManager()
    manager.addItsAccoount(masterid, itsacc)
    return itsaccounts(masterid)


@account_request_api.route("/additsaccountmobile", methods=["POST"])
def additsaccountmobile():
    itsacc = dbhelper.ITSAccount()
    masterId = request.form.get('masterid')
    itsAccNo = request.form.get('itsaccno')
    itsAccPass = request.form.get('itsaccpass')
    itsacc.itsNo = itsAccNo
    itsacc.password = itsAccPass
    manager = dbhelper.DBManager()
    manager.addItsAccoount(masterId, itsacc)
    return "success"


@account_request_api.route("/deleteitsaccount", methods=["POST"])
def deleteItsAccount():
    masterid = request.form.get('masterid')
    itsid = request.form.get('itsid')
    manager = dbhelper.DBManager()
    manager.deleteItsId(masterid, itsid)

    return "success"


@account_request_api.route("/<masterid>/clientids/")
@flask_login.login_required
def clientids(masterid):
    manager = dbhelper.DBManager()
    return render_template("clientids.html", masterid=masterid, clientids=manager.getClientIds(masterid))


@account_request_api.route("/<masterid>/addclientid", methods=["POST"])
def addclientid(masterid):
    client = dbhelper.Clientid()
    client.clientidno = request.form.get("clientid")
    manager = dbhelper.DBManager()
    manager.addClientId(masterid, client)
    return clientids(masterid)


@account_request_api.route("/clientids", methods=["POST"])
def getClientIDsMobile():
    masterid = request.form.get('masterid')
    masterpass = request.form.get('masterpass')
    manager = dbhelper.DBManager()
    clientIds = manager.getClientIdsMobile(masterid, masterpass)
    ids = []
    for id in clientIds:
        ids.append(id.clientidno)

    return json.dumps(ids)


@account_request_api.route("/updateitspassword", methods=["POST"])
def updateItsAccount():
    masterid = request.form.get('masterid')
    itsid = request.form.get('itsid')
    itspass = request.form.get('newitspass')
    manager = dbhelper.DBManager()
    return manager.updateItsId(masterid, itsid, itspass)
