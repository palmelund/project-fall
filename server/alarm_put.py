from model.alarm import deserialize as alarm_deserializer
import json
from server.respond import respond


def lambda_handler(event, context):
    try:
        alm = alarm_deserializer(json.loads(event["alarm"]))

        if alm.responder:
            alm.set()

            # TODO: Notify that someone has responded

        return respond("200", alm.serialize())
    except:
        return respond("400", event["alarm"])
