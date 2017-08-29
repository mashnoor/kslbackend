from flask import Flask, request

import flask

from loginapi import login_api
import dbhelper

import flask_login

login_manager = flask_login.LoginManager()

# Flask app should start in global layout
app = Flask(__name__)
app.register_blueprint(login_api)




@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    return flask.render_template('dashboard.html')


@app.route("/requestaccount", methods=["POST"])
def requestaccount():
    acc = dbhelper.Account()
    acc.email = request.form.get("email")
    acc.mobile = request.form.get("mobile")
    acc.password = request.form.get("password")
    acc.username = request.form.get("username")
    dbhelper.saveAccount(acc)
    return "Request for account creation in successful"


@app.route("/accounts")
def users():
    print dbhelper.getAccounts()
    return flask.render_template("accounts.html", accounts=dbhelper.getAccounts())


if __name__ == '__main__':
    port = 5003

    # print("Starting app on port %d" % port)

    app.run(port=port)
    # app.run(host='0.0.0.0', port=port)
