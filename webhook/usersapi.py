from flask import Blueprint, render_template

accounts_api = Blueprint('accounts_api', __name__)


@accounts_api.route("/")
def viewAccounts():
    return render_template("accounts.html")

