from model.device import deserialize
from model import device, user
from server.respond import respond
import json

# TODO: Fix me!

def lambda_handler(event, context):
    try:
        dvc = deserialize(event["device"])

        content = json.loads(dvc.content)

        if content["devicetype"] == "alexadevice":
            dvc: device.Device = device.Device.get_from_object(content)
            usr = dvc.get_owner()

            return respond("200", usr.serialize())

        # TODO: Add more devices

        else:
            return respond("400", user.User(-1, "", "", "userAdmin").serialize())
    except:
        return respond("400", user.User(-1, "", "", "userAdmin").serialize())
