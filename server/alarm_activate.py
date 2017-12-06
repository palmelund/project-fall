from model.alarm import deserialize as alarm_deserializer
from model.user import deserialize as user_deserializer
import boto3
from sns.sns_interface import push_message
# from sns.sns_interface import send_sms
from sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key
from respond import respond
import urllib.request
from endpoints import arn_alarm_create_endpoint
import json
from pprint import pprint


def lambda_handler(event, context):
    try:
        ctz = user_deserializer(event["citizen"])  # user.deserialize(json.loads(event["citizen"]))
    except Exception as ex:
        return respond("400", str(ex))

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
    except Exception as ex:
        return respond("400", str(ex))

    # Get the alarm
    try:

        alm = alarm_deserializer(json.load(data))

        # # TODO: WHAT?!?!??!?!
        # pprint(data)
        # load = json.loads(json.loads(data))
        # alm = deserialize(load)
    except Exception as ex:
        return respond("400", str(ex))

    # Send notifications
    for c in alm.activatedby.contacts:
        notify(alm.activatedby, c)

    # Send IFTTT event to citizen devices
    for d in alm.activatedby.devices:
        if d.messagetype == "ifttt":
            content = json.loads(d.content)
            urllib.request.urlopen(
                "https://maker.ifttt.com/trigger/fall_detected/with/key/" + json.loads(d.content)["key"]).read()
            break

    return respond("200", alm.serialize())


def message_builder(citizen):
    return citizen.name + " has had an falling accident, and requests help."


def notify(citizen, contact):
    for d in contact.devices:
        if d.devicetype == "smartphone":
            content = json.loads(d.content)
            if d.messagetype == "notification":
                push_message(content["arn"], message_builder(citizen))
            # elif d.messagetype == "sms":
                # Disabled sms since we pay per sms when sending outside US.
                # send_sms(content["number"], message_builder(citizen))
