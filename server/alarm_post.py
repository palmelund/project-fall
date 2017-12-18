import json
import urllib.request

import boto3
from server.sns.sns_interface import push_message
#from server.sns.sns_interface import send_sms

from model import alarm
from model.alarm import deserialize as alarm_deserializer
from model import user
from server.endpoints import arn_alarm_post_endpoint
from server.respond import respond
from server.sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key


def lambda_handler(event, context):
    try:
        ctz_id = int(event["id"])
    except:
        return respond("400", alarm.Alarm(-1, None, None).serialize())

    if not ctz_id:
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
            FunctionName=arn_alarm_post_endpoint,
            InvocationType="RequestResponse",
            Payload=arg)

        data = response["Payload"].read().decode()
    except:
        return respond("400", alarm.Alarm(-1, None, None).serialize())

    # Get the alarm
    try:
        dt = json.loads(json.loads(data))
        usr = user.deserialize(str(dt["activatedby"])) #user.Citizen(str(dt["activatedby"]).replace("'", '"'))
        alm = alarm.Alarm(dt["status"], usr, None)
    except:
        return respond("400", alarm.Alarm(-1, None, None).serialize())

    for c in alm.activatedby.contacts:
        for d in c.devices:
            if d.devicetype == "appdevice":
                if not d.arn or not d.token:
                    continue
                push_message(d.arn, alm.serialize())
            # elif d.devicetype == "smsdevice":
                # send_sms(d.phone_number, c.activatedby.name + " has had an falling accident, and requests help.")

    for d in alm.activatedby.devices:
        if d.devicetype == "iftttdevice":
            urllib.request.urlopen(
                "https://maker.ifttt.com/trigger/fall_detected/with/key/" + d.token).read()

    return respond("200", alm.serialize())
