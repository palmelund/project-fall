from model import device, user
from server.respond import respond
import json


def lambda_handler(event, context):
    try:
        dvc = device.deserialize(json.loads(event["device"]))
        usr = user.User.get(event["id"])
    except:
        return respond("400", device.Device(-1, "", "", ""))

    if not all(x is not None for x in [dvc, usr]):
        return respond("400", device.Device(-1, "", "", ""))

    dvc.set(usr)

    return respond("200", usr.get(usr.id).serialize())
