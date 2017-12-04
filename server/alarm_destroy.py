import json
from model.alarm import Alarm
from model.alarm import deserialize as alarm_deserializer
from database.database_manager import remove_alarm
from respond import build_response_no_ser

def lambda_handler(event, context):
    try:
        alm: Alarm = alarm_deserializer(json.loads(event["alarm"]))
        remove_alarm(alm.activatedby)
        return build_response_no_ser("200", {"status": "ok"})
    except Exception as ex:
        return build_response_no_ser("400", {"status": "error"})

