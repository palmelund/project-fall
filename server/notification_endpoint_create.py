from model.user import User
from model import user, device
from server.respond import respond
from server.endpoints import arn_notification_endpoint_store_endpoint
from server.sns.sns_interface import create_endpoint, update_endpoint
from server.sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key
import json
import boto3


def lambda_handler(event, context):
    try:
        dvc: device.AppDevice = device.deserialize(event["device"])

        if not dvc.arn:
            # Create arn
            arn_endpoint = create_endpoint(dvc.token)

            dvc.arn = arn_endpoint

            return respond("200", dvc.serialize())
        else:
            # Update arn
            update_endpoint(dvc.arn, dvc.token)
            return respond("200", dvc.serialize())
    except:
        return respond("400", "")



        if not usr or not dvc or dvc.devicetype != "appdevice":
            return respond("400", "")

    except:
        return respond("400", "")

    lambda_client = boto3.client('lambda',
                                 region_name=region_name,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)

    try:


        arg = bytes(json.dumps({"action": "create", "user": usr.serialize(), "device": dvc.serialize()}), 'utf-8')

        response = lambda_client.invoke(
            FunctionName=arn_notification_endpoint_store_endpoint,
            InvocationType="RequestResponse",
            Payload=arg)

        data = response["Payload"].read().decode()
        res = json.loads(data)

        if res == "ok":
            return respond("200", "")
        else:
            return respond("400", "")

    except Exception as ex:
        return respond("400", "")
