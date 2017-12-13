from model.alarm import deserialize as alarm_deserializer
import json
from server.respond import respond
import boto3
from server.sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key
from server.sns.sns_interface import push_message
from server.endpoints import arn_alarm_put_endpoint


def lambda_handler(event, context):
    try:
        alm = alarm_deserializer(json.loads(event["alarm"]))

        lambda_client = boto3.client('lambda',
                                     region_name=region_name,
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key)

        arg = bytes(json.dumps({"alarm": alm.serialize}), 'utf-8')
        response = lambda_client.invoke(
            FunctionName=arn_alarm_put_endpoint,
            InvocationType="RequestResponse",
            Payload=arg)

        data = response["Payload"].read().decode()

        if not data:
            return respond("400", event["alarm"])

        alm = alarm_deserializer(json.loads(data))

        if alm.responder:
            for d in alm.activatedby.devices:
                if d.devicetype == "appdevice":
                    if not d.arn or not d.token:
                        continue
                    push_message(d.arn, alm.serialize())

        return respond("200", alm.serialize())
    except:
        return respond("400", event["alarm"])
