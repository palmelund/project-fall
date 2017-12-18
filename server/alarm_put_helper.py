from model.alarm import deserialize as alarm_deserializer
import json
from server.respond import respond


def lambda_handler(event, context):
    try:
        alm = alarm_deserializer(json.loads(event["alarm"]))

        if alm.responder:
            alm.set()

        return alm.serialize()
    except:
        return None
