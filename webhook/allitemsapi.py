from flask import Blueprint, redirect
from flask import request, render_template, redirect, url_for
import dbhelper, json
from pathlib import Path
import flask_login
import datetime

allitems_api = Blueprint('allitems_api', __name__)


@allitems_api.route('/kslnews')
@flask_login.login_required
def kslnews():
    # p = '/var/www/html/kslbackend/ksl_news.txt'
    p = Path('../allitems.txt')
    with open(p) as f:
        content = f.read()

    allitems = json.loads(content)
    return render_template('kslnews.html', allitems=allitems)


@allitems_api.route('/addkslnews', methods=['POST'])
def addkslnews():
    company = request.form.get('item')
    # p = '/var/www/html/kslbackend/ksl_news.txt'
    p = Path('../allitems.txt')
    with open(p) as f:
        content = f.read()

    allItmes = json.loads(content)
    newItem = {}
    newItem['company'] = company
    allItmes.append(newItem)
    with open(p, 'w') as f:
        f.write(json.dumps(allNews, default=str))
    return redirect(url_for('kslnews_api.kslnews'))
