from flask import Blueprint
from flask import request, render_template, redirect, url_for
import flask_login

login_api = Blueprint('login_api', __name__)
users = {'keltu': {'password': 'keltu9876'}}

class User(flask_login.UserMixin):
    pass

@login_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
         return render_template('login.html')

    username = request.form['username']
    if request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('dashboard'))

    return "Your credentials didn't match :3"

@login_api.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))