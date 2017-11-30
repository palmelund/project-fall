from model.alarm import deserialize
from model import device, user
from model.user import Citizen
import boto3
import json
from sns.sns_interface import push_message, send_sms
from sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key
from respond import respond, build_response_no_ser
import urllib.request
from json_serializer import JsonSerializer
from endpoints import arn_alarm_create_endpoint


def lambda_handler(event, context):
    try:
        ctz: Citizen = user.deserialize(json.loads(event["citizen"]))
    except Exception as ex:
        build_response_no_ser("400", {"status": "error"})

    # Create alarm
    # To create an alarm, we need database access, so it has to happen on another VPC enabled lambda.
    # But if we are VPC enabled we are unable to interact with SNS services, so we have to split the task up.
    try:
        lambda_client = boto3.client('lambda',
                                     region_name=region_name,
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key)

        dump = json.dumps(ctz.working_serializer(), cls=JsonSerializer)
        arg = bytes(json.dumps({"citizen": dump}), 'utf-8')
        response = lambda_client.invoke(
            FunctionName=arn_alarm_create_endpoint,
            InvocationType="RequestResponse",
            Payload=arg)

        data = response["Payload"].read().decode()
    except Exception as ex:
        build_response_no_ser("400", {"status": "error"})

    # Get the alarm
    try:
        load = json.loads(json.loads(data))
        alm = deserialize(load)
    except Exception as ex:
        build_response_no_ser("400", {"status": "error"})

    # Send notifications
    for c in alm.activatedby.contacts:
        notify(alm.activatedby, c)

    # Send IFTTT event to citizen devices
    for d in alm.activatedby.devices:
        content = json.loads(d.content)
        if content["messagetype"] == "ifttt":
            urllib.request.urlopen(
                "https://maker.ifttt.com/trigger/fall_detected/with/key/" + json.loads(d.content)["key"]).read()

    # Return
    return build_response_no_ser("200", alm.serialize())


def message_builder(citizen):
    # TODO: Better message
    return citizen.name + " has had an falling accident, and requests help."


def notify(citizen, contact):
    for d in contact.devices:
        if d.content:
            content = json.loads(d.content)
            if content["messagetype"] == "sms":
                send_sms(content["number"], message_builder(citizen))
            elif content["messagetype"] == "notification":
                push_message(content["arn"], message_builder(citizen))
                # If it is neither, do nothing
