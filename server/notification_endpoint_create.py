from model.user import User
from model import user
from respond import build_response_no_ser
from endpoints import arn_notification_endpoint_store_endpoint
from sns.sns_interface import create_endpoint
from sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key
import json
import boto3


def lambda_handler(event, context):
    try:
        usr: User = user.deserialize(json.loads(event["user"]))
        token = event["token"]
    except Exception as ex:
        return build_response_no_ser("400", "")

    lambda_client = boto3.client('lambda',
                                 region_name=region_name,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)

    try:
        arn_endpoint = create_endpoint(token)

        arg = bytes(json.dumps({"messagetype": "notification", "token": token, "arn": arn_endpoint, "action": "create", "citizen": usr.serialize()}), 'utf-8')

        response = lambda_client.invoke(
            FunctionName=arn_notification_endpoint_store_endpoint,
            InvocationType="RequestResponse",
            Payload=arg)

        data = response["Payload"].read().decode()
        res = json.loads(data)

        if res["status"] == "ok":
            return build_response_no_ser("200", "")
        else:
            return build_response_no_ser("400", "")

    except Exception as ex:
        return build_response_no_ser("400", "")
