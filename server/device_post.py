from model import device, user
from server.respond import respond
import json


def lambda_handler(event, context):
    try:
        dvc = device.deserialize(event["device"])
        usr = user.User.get(event["id"])
    except:
        return respond("400", device.Device(-1, "", "", "").serialize())

    if not all(x is not None for x in [dvc, usr]):
        return respond("400", device.Device(-1, "", "", "").serialize())

    dvc.post(usr)

    return respond("200", dvc.serialize())
