import requests
from model.user import Citizen
from model import user
from model import device
from sns.sns_interface import update_endpoint
import json
import boto3
from endpoints import arn_notification_endpoint_store_endpoint
from respond import build_response_no_ser

def lambda_handler(event, context):
    try:
        usr = user.deserialize(json.loads(event["user"]))
        oldtoken = event["oldtoken"]
        newtoken = event["newtoken"]

    except Exception as ex:
        return build_response_no_ser("400", "error")

    lambda_client = boto3.client('lambda',
                                 region_name=region_name,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)

    try:
        for dvc in usr.devices:
            content = device.deserialize(dvc)
            if content["devicetype"] == "smartphone" and content["messagetype"] == "notification" and content["token"] == oldtoken:
                content["token"] = newtoken

                update_endpoint(content["arn"], newtoken)

                dump = json.dumps({"messagetype": "notification", "token": newtoken, "arn": content["arn"], "action": "create"})
                arg = bytes(json.dumps({"citizen": dump}), 'utf-8')

                response = lambda_client.invoke(
                    FunctionName=arn_notification_endpoint_store_endpoint,
                    InvocationType="RequestResponse",
                    Payload=arg)

                data = response["Payload"].read().decode()
                res = json.loads(data)

                if res["status"] == "ok":
                    return build_response_no_ser("200", "ok")
                else:
                    return build_response_no_ser("400", "error")
    except Exception as ex:
        return ex