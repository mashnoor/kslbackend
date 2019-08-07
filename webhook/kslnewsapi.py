from flask import Blueprint, redirect
from flask import request, render_template, redirect, url_for
import dbhelper, json
import flask_login
import datetime

import settings

kslnews_api = Blueprint('kslnews_api', __name__)


@kslnews_api.route('/kslnews')
@flask_login.login_required
def kslnews():
    p = settings.static_backend_path + 'ksl_news.txt'

    with open(p) as f:
        content = f.read()

    allNews = json.loads(content)
    allNews.reverse()
    return render_template('kslnews.html', allNews=allNews)


@kslnews_api.route('/addkslnews', methods=['POST'])
def addkslnews():
    title = request.form.get('title')
    body = request.form.get('message')
    p = settings.static_backend_path + 'ksl_news.txt'

    with open(p) as f:
        content = f.read()

    allNews = json.loads(content)
    newNews = {}
    newNews['title'] = title
    newNews['body'] = body
    newNews['date'] = datetime.date.today()
    allNews.append(newNews)
    with open(p, 'w') as f:
        f.write(json.dumps(allNews, default=str))
    return redirect(url_for('kslnews_api.kslnews'))
