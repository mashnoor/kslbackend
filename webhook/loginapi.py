from flask import Blueprint
from flask import request, render_template, redirect, url_for
import flask_login, dbhelper

login_api = Blueprint('login_api', __name__)


@login_api.route("/masterlogin", methods=["POST"])
def master_login():
    masterid = request.form.get('masterid')
    masterpass = request.form.get('masterpass')
    if dbhelper.isValiedMasterId(masterid, masterpass):
        return "success"
    else:
        return "failed"


@login_api.route("/settoken", methods=["POST"])
def settoken():
    token = request.form.get('token')
    masterId = request.form.get('masterid')
    dbhelper.setToken(masterId, token)
    return "success"
