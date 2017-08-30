from flask import Blueprint, render_template, request
import dbhelper

requisitions_api = Blueprint('requisitions_api', __name__)


@requisitions_api.route("/requisitions")
def requisitions():
    return render_template("fundrequisitions.html", requisitions=dbhelper.getRequisitions())

@requisitions_api.route("/requestrequisition", methods=["POST"])
def requestrequisition():
    req_json = request.get_json()
    new_requisition = dbhelper.FundRequisition()
    new_requisition.itsaccno = req_json["itsaccno"]
    new_requisition.amount = req_json["amount"]
    new_requisition.reqdate = req_json["reqdate"]
    new_requisition.isApproved = 0
    dbhelper.saveRequisitionRequest(new_requisition)
    return "Successfully Saved"

