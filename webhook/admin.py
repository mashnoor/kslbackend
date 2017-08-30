from flask import Flask, request, render_template

import flask

from loginapi import login_api

import flask_login
from requisitions import requisitions_api
from accountrequests import account_request_api

login_manager = flask_login.LoginManager()

# Flask app should start in global layout
app = Flask(__name__)
app.register_blueprint(login_api)
app.register_blueprint(requisitions_api)
app.register_blueprint(account_request_api)


@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    return flask.render_template('dashboard.html')


if __name__ == '__main__':
    port = 5003
    # print("Starting app on port %d" % port)
    app.run(port=port)
    # app.run(host='0.0.0.0', port=port)
