from model import alarm
from model import device
from model import user
from respond import build_response_no_ser
from sns import sns_interface
import urllib.request
import json


def lambda_handler(event, context):
    _device = deserialize(json.loads(event["device"]))
    _user = deserialize(json.loads(event["user"]))

    _device.set(_user)

    return build_response_no_ser("200", user.get(_user.id).serialize())
