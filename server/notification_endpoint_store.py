from model import user, device
from model.device import Device
from server.database.database_manager import get_user_devices
import json


def lambda_handler(event, context):
    try:
        dvc = device.deserialize(json.loads(event["device"]))
        action = event["action"]

        if action == "create":
            dvc.put()

        elif action == "update":
            dvc.update()


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
