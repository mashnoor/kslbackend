from flask import Flask, request, render_template

import flask

from loginapi import login_api

import flask_login
from requisitions import requisitions_api
from accountrequests import account_request_api
from notification import notification_api
from portfoliostatement import portfoliostatement_api
from pyfcm import FCMNotification

login_manager = flask_login.LoginManager()

# Flask app should start in global layout
app = Flask(__name__)
app.register_blueprint(login_api)
app.register_blueprint(requisitions_api)
app.register_blueprint(account_request_api)
app.register_blueprint(notification_api)
app.register_blueprint(portfoliostatement_api)


@app.route('/abc')
def dashboard():

    return "OK"


if __name__ == '__main__':
    port = 5003
    # print("Starting app on port %d" % port)
    app.run(port=port)
    # app.run(host='0.0.0.0', port=port)
