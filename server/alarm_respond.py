from model.alarm import Alarm
from model.alarm import deserialize as alarm_deserializer
import json
from respond import build_response_no_ser


def lambda_handler(event, context):
    try:
        alm: Alarm = alarm_deserializer(json.loads(event["alarm"]))

        if alm.responder:
            alm.set()

            # TODO: Notify that someone has responded

        return build_response_no_ser("200", "")
    except Exception as ex:
        return build_response_no_ser("400", "")
