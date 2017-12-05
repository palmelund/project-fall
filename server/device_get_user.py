from model.device import deserialize
from model import device
from respond import build_response
from json_serializer import JsonSerializer
import json


def lambda_handler(event, context):
    try:
        inputdevice = deserialize(json.loads(event["device"]))

        content = json.loads(inputdevice.content)

        if content["messagetype"] != "input":
            return build_response("400", {"status": "error 1"})

        if content["devicetype"] == "alexa":
            dvc: device.Device = device.Device.get_from_object(content)
            usr = dvc.get_owner()

            return build_response("200", json.dumps(usr.working_serializer(), cls=JsonSerializer))

        else:
            return build_response("400", {"status": "error 2"})
    except Exception as ex:
        return build_response("400", {"status": "error 3"})
