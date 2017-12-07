import json
import urllib.request

import boto3

from model import alarm
from model.alarm import deserialize as alarm_deserializer
from model.user import deserialize as user_deserializer
from server.endpoints import arn_alarm_create_endpoint
from server.respond import respond
from server.sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key


def lambda_handler(event, context):
    try:
        ctz = user_deserializer(event["citizen"])  # user.deserialize(json.loads(event["citizen"]))
    except:
        return respond("400", alarm.Alarm(-1, None, None).serialize())

    # Create alarm
    # To create an alarm, we need database access, so it has to happen on another VPC enabled lambda.
    # But if we are VPC enabled we are unable to interact with SNS services, so we have to split the task up.
    try:
        lambda_client = boto3.client('lambda',
                                     region_name=region_name,
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key)

        dump = ctz.serialize()
        arg = bytes(json.dumps({"citizen": dump}), 'utf-8')
        response = lambda_client.invoke(
            FunctionName=arn_alarm_create_endpoint,
            InvocationType="RequestResponse",
            Payload=arg)

        data = response["Payload"].read().decode()
    except:
        return respond("400", alarm.Alarm(-1, ctz.serialize(), None).serialize())

    # Get the alarm
    try:
        alm = alarm_deserializer(json.load(data))
    except:
        return respond("400", alarm.Alarm(-1, ctz.serialize(), None).serialize())

    # Send notifications
    for c in alm.activatedby.contacts:
        c.notify(alm.activatedby)

    # Send IFTTT event to citizen devices
    for d in alm.activatedby.devices:
        if d.messagetype == "ifttt":
            content = json.loads(d.content)
            urllib.request.urlopen(
                "https://maker.ifttt.com/trigger/fall_detected/with/key/" + json.loads(d.content)["key"]).read()
            break

    return respond("200", alm.serialize())
