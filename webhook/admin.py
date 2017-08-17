
from flask import Flask

import flask

from loginapi import login_api
import dbhelper

import flask_login
login_manager = flask_login.LoginManager()



# Flask app should start in global layout
app = Flask(__name__)
app.register_blueprint(login_api)


from sqlalchemy.orm import sessionmaker
@app.route('/dashboard')
@flask_login.login_required
def dashboard():

        return flask.render_template('dashboard.html')

@app.route("/users")
def users():
    u = dbhelper.User()
    u.username = "Vabi"
    u.email = "vabi@gmail.com"
    u.mobile = "018777777"
    u.isApproved = 1
    #dbhelper.saveUser(u)
    print dbhelper.getUsers()
    return flask.render_template("accounts.html", users=dbhelper.getUsers())



if __name__ == '__main__':
    port = 5003

    #print("Starting app on port %d" % port)

    app.run(port=port)
    #app.run(host='0.0.0.0', port=port)
