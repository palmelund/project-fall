from respond import respond, build_response_no_ser
import json
from model.alarm import *
from model import alarm


def lambda_handler(event, context):
    try:
        alm = alarm.deserialize(json.loads(event["alarm"]))
    except Exception as ex:
        print (str(ex))
        return build_response_no_ser("400", "Missing arguments 1!")

    if not alm:
        return build_response_no_ser("400", "Missing arguments 2!")

    alm.set()

    return respond(None)
