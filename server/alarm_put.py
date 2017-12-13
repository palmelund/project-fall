from model.alarm import deserialize as alarm_deserializer
import json
from server.respond import respond
import boto3
from server.sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key
from server.sns.sns_interface import push_message
from server.endpoints import arn_alarm_put_endpoint
from pprint import pprint


def lambda_handler(event, context):
    try:
        print("STEP 0: STARTING")
        alm = alarm_deserializer(event["alarm"])
        pprint(event)

        print("STEP 1: PREPARING CLIENT")
        lambda_client = boto3.client('lambda',
                                     region_name=region_name,
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key)

        print("STEP 2: PACKING ARGUMENT")
        arg = bytes(json.dumps({"alarm": alm.serialize()}), 'utf-8')

        print("STEP 3: INVOKING")
        response = lambda_client.invoke(
            FunctionName=arn_alarm_put_endpoint,
            InvocationType="RequestResponse",
            Payload=arg)

        print("STEP 4: GETTING RESPONSE")
        data = response["Payload"].read().decode()

        print("STEP 5: DATA")
        pprint(data)

        if not data:
            print("STEP 6a: NOT DATA")
            return respond("400", event["alarm"])

        print("STEP 6b: DESERIALIZING DATA")
        alm = alarm_deserializer(json.loads(data))

        print("STEP 7: REPLY IF RESPONDER")
        if alm.responder:
            for d in alm.activatedby.devices:
                print("STEP 8: NOTIFYING")
                pprint(d)
                if d.devicetype == "appdevice":
                    if not d.arn or not d.token:
                        continue
                    print("STEP 9: PUSHING")
                    try:
                        print(type(d.arn))
                        print(d.arn)
                        print(alm.responder.serialize())
                        print(type(alm.responder.serialize()))

                        push_message(d.arn, alm.responder.serialize())
                    except:
                        print(
                            "Failed to push notification: CitizenID: " + str(alm.activatedby.id) + " Device ID: " + str(
                                d.id))

        print("STEP 9: RETURNING")
        return respond("200", alm.serialize())
    except Exception as ex:
        print("STEP -1: SOMETHING WENT WRONG")
        raise ex
        pprint(ex)

        return respond("400", event["alarm"])
