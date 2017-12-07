import json
from model import alarm
from model.alarm import deserialize as alarm_deserializer
from server.respond import respond


def lambda_handler(event, context):
    try:
        alm = alarm_deserializer(event["alarm"])
        alm.delete()
        return respond("200", alarm.Alarm(-1, alm.activatedby, None).serialize())
    except:
        return respond("400", event["alarm"])
