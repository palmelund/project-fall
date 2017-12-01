from model import user
from model.user import Citizen
from model.device import Device
from database.database_manager import get_user_devices
import json


def lambda_handler(event, context):
    try:
        usr = user.deserialize(json.loads(event["citizen"]))
        messagetype = event["messagetype"]
        token = event["token"]
        arn = event["arn"]
        action = event["action"]

        if action == "create":
            dvc: Device = Device(0, json.dumps({"messagetype": messagetype, "token": token, "arn": arn}))
            dvc.put(usr)

        elif action == "update":
            devices = get_user_devices(usr.id)
            for d in devices:
                content = json.loads(d.content)
                if content["arn"] == arn:
                    content["token"] = token
                    d.content = json.dumps(content)
                    d.update(usr)
                    break

        else:
            return {"status", "failure"}

        return {"status": "ok"}

    except Exception as ex:
        return {"status", "failure"}
