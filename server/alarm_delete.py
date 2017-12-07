import json
from model import alarm
from model.alarm import deserialize as alarm_deserializer
from server.database.database_manager import delete_alarm
from server.respond import respond

def lambda_handler(event, context):
    try:
        alm = alarm_deserializer(json.loads(event["alarm"]))
        delete_alarm(alm.activatedby)
        return respond("200", alarm.Alarm(-1,alm.activatedby,None).serialize())
    except:
        return respond("400", event["alarm"])

