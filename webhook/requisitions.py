from flask import Blueprint, render_template, request
import dbhelper

requisitions_api = Blueprint('requisitions_api', __name__)


@requisitions_api.route("/requisitions")
def requisitions():
    return render_template("fundrequisitions.html", requisitions=dbhelper.getRequisitions())


@requisitions_api.route("/requestrequisition", methods=["POST"])
def requestrequisition():
    new_requisition = dbhelper.FundRequisition()
    new_requisition.itsaccno = request.form.get("itsaccno")  # itsacc supposed to be client id
    new_requisition.amount = request.form.get('amount')
    new_requisition.reqdate = request.form.get('date')
    new_requisition.isApproved = 0
    dbhelper.save(new_requisition)
    return "Successfully Saved"
