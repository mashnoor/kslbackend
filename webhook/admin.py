from flask import Flask

from requisitions import requisitions_api
from accountrequests import account_request_api
from notification import notification_api
from portfoliostatement import portfoliostatement_api
from pyfcm import FCMNotification
from orderstatusparse import getorderstatus_api
from get_previous_day_end_data import previous_day_end_data_api
from get_item_details import get_item_detail_api
from financialledger import financial_ledger_api
from market_depth import market_depth_api

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


@app.route('/abc')
def dashboard():
    return "OK"


if __name__ == '__main__':
    port = 5003
    # print("Starting app on port %d" % port)
    app.run(port=port)
    # app.run(host='0.0.0.0', port=port)
