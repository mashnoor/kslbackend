from flask import Blueprint, render_template, request
import dbhelper
import flask_login
import requests, json

requisitions_api = Blueprint('requisitions_api', __name__)


@requisitions_api.route("/requisitions")
@flask_login.login_required
def requisitions():
    return render_template("fundrequisitions.html", requisitions=dbhelper.getRequisitions())


@requisitions_api.route("/requestrequisition", methods=["POST"])
def requestrequisition():
    url = "http://api.kslbd.net:88/client/requisition/insert/sandbox/sandbox/sandbox/"
    new_requisition = {}
    new_requisition['app_id'] = 5436
    new_requisition['title'] = 'TEST'
    new_requisition['description'] = 'TEST'
    new_requisition['client_id'] = request.form.get("clientid")  # itsacc supposed to be client id
    new_requisition['requisition_amount'] = request.form.get('amount')
    new_requisition['disbursement_date'] = request.form.get('date')
    new_requisition['routing_number'] = ""
    new_requisition['explanation'] = "TEST"

    r = requests.get(url+json.dumps(new_requisition))

    print(r.content)

    return "Successfully Saved"
