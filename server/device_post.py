from model import device, user
from server.respond import respond
import json


def lambda_handler(event, context):
    try:
        dvc = device.deserialize(json.loads(event["device"]))
        usr = user.deserialize(json.loads(event["user"]))
    except:
        return respond("400", event["user"])

    dvc.set(usr)

    return respond("200", usr.get(usr.id).serialize())
