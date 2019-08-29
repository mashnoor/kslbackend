from flask import Blueprint
from flask import request, render_template, redirect, url_for
import dbhelper, json

login_api = Blueprint('login_api', __name__)


@login_api.route("/masterlogin", methods=["POST"])
def master_login():
    masterid = request.form.get('masterid')
    masterpass = request.form.get('masterpass')
    manager = dbhelper.DBManager()
    if manager.isValiedMasterId(masterid, masterpass):
        acc = manager.getMasterAccount(masterid, masterpass)
        retAcc = {}
        retAcc['masterid'] = acc.masterId
        retAcc['masterpass'] = acc.masterPassword
        retAcc['name'] = acc.name

        return json.dumps(retAcc)
    else:
        return "failed"


@login_api.route("/settoken", methods=["POST"])
def settoken():
    token = request.form.get('token')
    masterId = request.form.get('masterid')
    manager = dbhelper.DBManager()
    manager.setToken(masterId, token)
    return "success"
