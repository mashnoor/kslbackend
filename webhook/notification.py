from flask import Blueprint, render_template, request, redirect, url_for
import dbhelper
import json
import datetime
from pyfcm import FCMNotification

notification_api = Blueprint('notification_api', __name__)


@notification_api.route("/individualnotification")
def individualnotification():
    return render_template("individualnotification.html", accounts=dbhelper.getMasterAccounts())


@notification_api.route("/groupnotification")
def groupnotification():
    return render_template("groupnotification.html", accounts=dbhelper.getMasterAccounts())


@notification_api.route("/addnotification", methods=["POST"])
def addnotification():
    masterid = request.form.get("masterid")
    message = request.form.get("message")
    newNotification = dbhelper.Notification()
    newNotification.message = message
    newNotification.sendTimestamp = datetime.datetime.now()
    dbhelper.addNotification(masterid, newNotification)

    return masterid + " - " + message


@notification_api.route("/settoken", methods=["POST"])
def settoken():
    r = request.get_json()
    token = r["token"]
    masterId = r["masterid"]
    dbhelper.setToken(masterId, token)
    return "success"


@notification_api.route("/sendsinglenotification", methods=["POST"])
def sendsinglenotification():
    push_service = FCMNotification(
        api_key="AAAAYv7rBNM:APA91bEwGTAwNGMqqFnh_3YSrcbCFvcwXvxlJhdEumZQQ6RU7_PnBlbBZILJwWKEyXLOaKCgLUDXwMiPk8lx1ONWyzrcR1KI5fxLysyAgrgWsLPhPrFjsLYsEiV-rsD39OcMcwd_omvU_zIFI-ynM0j0_RKj0OgRqQ")

    masterid = request.form.get("masterid")
    token = dbhelper.getToken(masterid)

    message_title = request.form.get("title")
    message_body = request.form.get("message")

    newNotif = dbhelper.Notification()
    newNotif.title = message_title
    newNotif.message = message_body
    newNotif.sendTimestamp = datetime.datetime.now()
    dbhelper.addNotification(masterid, newNotif)
    result = push_service.notify_single_device(registration_id=token, message_title=message_title,
                                               message_body=message_body)

    print(result)
    return "Notifcation sent successfully"


@notification_api.route("/sendgroupnotification", methods=["POST"])
def sendgroupnotification():
    push_service = FCMNotification(
        api_key="AAAAYv7rBNM:APA91bEwGTAwNGMqqFnh_3YSrcbCFvcwXvxlJhdEumZQQ6RU7_PnBlbBZILJwWKEyXLOaKCgLUDXwMiPk8lx1ONWyzrcR1KI5fxLysyAgrgWsLPhPrFjsLYsEiV-rsD39OcMcwd_omvU_zIFI-ynM0j0_RKj0OgRqQ")

    masterids = request.form.getlist('masterid')
    tokens = []
    for masterid in masterids:
        tokens.append(str(dbhelper.getToken(masterid)))

    message_title = request.form.get("title")
    message_body = request.form.get("message")

    newNotif = dbhelper.Notification()
    newNotif.title = message_title
    newNotif.message = message_body
    newNotif.sendTimestamp = datetime.datetime.now()
    dbhelper.addGroupNotification(masterids, newNotif)

    result = push_service.notify_multiple_devices(registration_ids=tokens, message_title=message_title,
                                                  message_body=message_body)
    print(result)
    return "Notifcation sent successfully"


@notification_api.route("/getnotifications/<masterid>")
def getnotifications(masterid):
    notifications = dbhelper.getNotifications(masterid)
    notif = []
    for notification in notifications:
        curr_notif = {
            "title": notification.title,
            "message": notification.message,
            "time": notification.sendTimestamp
        }
        notif.append(curr_notif)

    return json.dumps(notif, default=str)
