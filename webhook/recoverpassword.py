import smtplib
from flask import Blueprint, render_template, request
import dbhelper, json
import datetime
import requests



recoverpassword_api = Blueprint('recoverpassword_api', __name__)


@recoverpassword_api.route('/recoverpassword', methods=['POST'])
def recoverPassword():
    email = request.form.get('email')
    masterid = request.form.get('masterid')
    curr_date_time = datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")

    try:
         password = dbhelper.getMasterPassword(email, masterid)
    except:
        return "error"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("kslapprecovery@gmail.com", "kslapprecovery1234")


    msg = "Hello " + masterid + \
          "\nA password recovery request was sent on " + \
          curr_date_time + " Your password is:\n\n" + \
        password + "\n\nRegards\nKSL App Team"
    server.sendmail("kslapprecovery@gmail.com", email, msg)
    server.quit()
    return "success"