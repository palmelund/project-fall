import json
import urllib.request

import boto3
from server.sns.sns_interface import push_message
# from server.sns.sns_interface import send_sms

from model import alarm
from model.alarm import deserialize as alarm_deserializer
from model import user
from server.endpoints import arn_alarm_create_endpoint
from server.respond import respond
from server.sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key


def lambda_handler(event, context):
    try:
        ctz_id = event["id"]  # user.deserialize(json.loads(event["citizen"]))
        alm = alarm_deserializer(event["alarm"])
    except:
        return respond("400", alarm.Alarm(-1, None, None).serialize())

    if not all(x is not None for x in [ctz_id, alm]) or ctz_id != alm.activatedby.id:
        return respond("400", alarm.Alarm(-1, None, None).serialize())

    # Create alarm
    # To create an alarm, we need database access, so it has to happen on another VPC enabled lambda.
    # But if we are VPC enabled we are unable to interact with SNS services, so we have to split the task up.
    try:
        lambda_client = boto3.client('lambda',
                                     region_name=region_name,
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key)

        arg = bytes(json.dumps({"id": ctz_id}), 'utf-8')
        response = lambda_client.invoke(
            FunctionName=arn_alarm_create_endpoint,
            InvocationType="RequestResponse",
            Payload=arg)

        data = response["Payload"].read().decode()
    except:
        return respond("400", alarm.Alarm(-1, None, None).serialize())

    # Get the alarm
    try:
        alm = alarm_deserializer(json.load(data))
    except:
        return respond("400", alarm.Alarm(-1, None, None).serialize())

    # Send notifications
    for c in alm.activatedby.contacts:
        notify(c, alm.activatedby)

    # Send IFTTT event to citizen devices
    for d in alm.activatedby.devices:
        if d.messagetype == "ifttt":
            content = json.loads(d.content)
            urllib.request.urlopen(
                "https://maker.ifttt.com/trigger/fall_detected/with/key/" + json.loads(d.content)["key"]).read()
            break

    return respond("200", alm.serialize())


def notify(cnt, ctz):
    for d in cnt.devices:
        if d.devicetype == "smartphone":
            content = json.loads(d.content)
            if d.messagetype == "notification":
                push_message(content["arn"], ctz.name + " has had an falling accident, and requests help.")
                # elif d.messagetype == "sms":
                # Disabled sms since we pay per sms when sending outside US.
                    # send_sms(content["number"], message_builder(citizen))