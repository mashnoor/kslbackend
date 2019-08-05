from flask import Flask, render_template, request, redirect, url_for

from requisitions import requisitions_api
from accountrequests import account_request_api
from notification import notification_api
from portfoliostatement import portfoliostatement_api

from orderstatusparse import getorderstatus_api
from get_previous_day_end_data import previous_day_end_data_api
from get_item_details import get_item_detail_api
from financialledger import financial_ledger_api
from market_depth import market_depth_api
from trade import trade_api
from get_item_news import get_item_news_api
from recoverpassword import recoverpassword_api
from loginapi import login_api
import flask_login
from kslnewsapi import kslnews_api
from ipoapi import ipo_api
import settings
# Flask app should start in global layout
app = Flask(__name__)

app.register_blueprint(requisitions_api)
app.register_blueprint(account_request_api)
app.register_blueprint(notification_api)
app.register_blueprint(portfoliostatement_api)
app.register_blueprint(getorderstatus_api)
app.register_blueprint(previous_day_end_data_api)
app.register_blueprint(get_item_detail_api)
app.register_blueprint(financial_ledger_api)
app.register_blueprint(market_depth_api)
app.register_blueprint(trade_api)
app.register_blueprint(get_item_news_api)
app.register_blueprint(recoverpassword_api)
app.register_blueprint(login_api)
app.register_blueprint(kslnews_api)
app.register_blueprint(ipo_api)

app.secret_key = 'ksl onek joss'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

users = {'ksladmin': {'password': 'kslappsecret'}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    if request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('dashboard'))

    return "Credentials didn't match. Contact with administration"


@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


@app.route('/test')
def test():
    l = []
    return l[1]


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


@app.errorhandler(404)
def notFound(error):
    return "<h1>Page Requested not found.</h1>"


if __name__ == '__main__':

    # print("Starting app on port %d" % port)
    app.run(host=settings.host, port=settings.port, threaded=True)
    # app.run(host='0.0.0.0', port=port)
