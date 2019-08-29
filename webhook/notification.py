from flask import Blueprint, render_template, request, redirect, url_for
import dbhelper
import json
import datetime
from pyfcm import FCMNotification
import flask_login

notification_api = Blueprint('notification_api', __name__)


@notification_api.route("/individualnotification")
@flask_login.login_required
def individualnotification():
    manager = dbhelper.DBManager()
    return render_template("individualnotification.html", accounts=manager.getMasterAccounts())


@notification_api.route("/groupnotification")
@flask_login.login_required
def groupnotification():
    manager = dbhelper.DBManager()
    return render_template("groupnotification.html", accounts=manager.getMasterAccounts())


@notification_api.route("/addnotification", methods=["POST"])
@flask_login.login_required
def addnotification():
    masterid = request.form.get("masterid")
    message = request.form.get("message")
    newNotification = dbhelper.Notification()
    newNotification.message = message
    newNotification.sendTimestamp = datetime.datetime.now()
    manager = dbhelper.DBManager()
    manager.addNotification(masterid, newNotification)

    return masterid + " - " + message


@notification_api.route("/settoken", methods=["POST"])
def settoken():
    token = request.form.get('token')
    masterId = request.form.get('masterid')
    manager = dbhelper.DBManager()
    manager.setToken(masterId, token)
    return "success"


@notification_api.route("/sendsinglenotification", methods=["POST"])
@flask_login.login_required
def sendsinglenotification():
    push_service = FCMNotification(
        api_key="AAAAYv7rBNM:APA91bEwGTAwNGMqqFnh_3YSrcbCFvcwXvxlJhdEumZQQ6RU7_PnBlbBZILJwWKEyXLOaKCgLUDXwMiPk8lx1ONWyzrcR1KI5fxLysyAgrgWsLPhPrFjsLYsEiV-rsD39OcMcwd_omvU_zIFI-ynM0j0_RKj0OgRqQ")

    masterid = request.form.get("masterid")
    manager = dbhelper.DBManager()
    token = manager.getToken(masterid)

    message_title = request.form.get("title")
    message_body = request.form.get("message")

    newNotif = dbhelper.Notification()
    newNotif.title = message_title
    newNotif.message = message_body
    newNotif.sendTimestamp = datetime.datetime.now()
    manager.addNotification(masterid, newNotif)
    result = push_service.notify_single_device(registration_id=token, message_title=message_title,
                                               message_body=message_body)

    print(result)
    return "Notifcation sent successfully"


@notification_api.route("/sendgroupnotification", methods=["POST"])
@flask_login.login_required
def sendgroupnotification():
    push_service = FCMNotification(
        api_key="AAAAYv7rBNM:APA91bEwGTAwNGMqqFnh_3YSrcbCFvcwXvxlJhdEumZQQ6RU7_PnBlbBZILJwWKEyXLOaKCgLUDXwMiPk8lx1ONWyzrcR1KI5fxLysyAgrgWsLPhPrFjsLYsEiV-rsD39OcMcwd_omvU_zIFI-ynM0j0_RKj0OgRqQ")

    masterids = request.form.getlist('masterid')
    manager = dbhelper.DBManager()
    tokens = []
    for masterid in masterids:
        tokens.append(str(manager.getToken(masterid)))

    message_title = request.form.get("title")
    message_body = request.form.get("message")

    newNotif = dbhelper.Notification()
    newNotif.title = message_title
    newNotif.message = message_body
    newNotif.sendTimestamp = datetime.datetime.now()
    manager.addGroupNotification(masterids, newNotif)

    result = push_service.notify_multiple_devices(registration_ids=tokens, message_title=message_title,
                                                  message_body=message_body)
    print(result)
    return "Notifcation sent successfully"


@notification_api.route("/getnotifications", methods=['POST'])
def getnotifications():
    masterid = request.form.get('masterid')
    manager = dbhelper.DBManager()
    notifications = manager.getNotifications(masterid)
    notif = []
    for notification in notifications:
        curr_notif = {
            "title": notification.title,
            "message": notification.message,
            "time": notification.sendTimestamp
        }
        notif.append(curr_notif)

    return json.dumps(notif, default=str)
