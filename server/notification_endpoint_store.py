from model import user, device
import json


def lambda_handler(event, context):
    try:

        action = event["action"]
        if action == "create":
            usr: user.User = user.deserialize(event["user"])

        dvc: device.AppDevice = device.deserialize(event["device"])

        if action == "create":
            dvc.post(usr)

        elif action == "update":
            dvc.put()
        else:
            return "failure"

        return "ok"

    except:
        return "failure"
