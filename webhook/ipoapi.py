

import flask_login
from flask import Blueprint
from flask import request, render_template, redirect, url_for
import settings

ipo_api = Blueprint('ipo_api', __name__)


@ipo_api.route('/ipo')
@flask_login.login_required
def ipo():
    p = settings.static_backend_path + 'ipo.txt'
    # p = Path('../ipo.txt')
    with open(p) as f:
        content = f.read()

    return render_template('ipo.html', ipo=content)


@ipo_api.route('/updateipo', methods=['POST'])
def updateipo():
    updatedIpo = request.form.get('ipo')
    p = settings.static_backend_path + 'ipo.txt'

    with open(p, 'w') as f:
        f.write(str(updatedIpo).replace("\n", ""))
    return redirect(url_for('ipo_api.ipo'))
