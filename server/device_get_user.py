from model.device import deserialize
from model import device
from respond import build_response
from json_serializer import JsonSerializer
import json


def lambda_handler(event, context):
    try:
        device = deserialize(json.loads(event["device"]))

        content = json.loads(device.content)

        if content["messagetype"] != "input":
            return build_response("400", {"status": "error"})

        if content["devicetype"] == "alexa":
            dvc = device.Device.get_from_object(content)

            return build_response("200", json.dumps(dvc.working_serializer(), cls=JsonSerializer))

        else:
            return build_response("400", {"status": "error"})
    except Exception as ex:
        return build_response("400", {"status": "error"})
