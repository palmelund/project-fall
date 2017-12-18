from model.device import deserialize
from model import device
from server.respond import respond
from server.sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key
import boto3
import json
from server.endpoints import arn_device_put_endpoint
from server.sns.sns_interface import create_endpoint, update_endpoint


def lambda_handler(event, context):
    try:
        dvc = deserialize(event["device"])

        if not dvc:
            return respond("400", event["device"])

        if dvc.devicetype == "appdevice":
            dvc: device.AppDevice = device.deserialize(event["device"])

            if not dvc.arn:
                # Create arn
                arn_endpoint = create_endpoint(dvc.token)
                dvc.arn = arn_endpoint
            else:
                # Update arn
                update_endpoint(dvc.arn, dvc.token)

            lambda_client = boto3.client('lambda',
                                         region_name=region_name,
                                         aws_access_key_id=aws_access_key_id,
                                         aws_secret_access_key=aws_secret_access_key)

            arg = bytes(json.dumps({"device": dvc.serialize()}), 'utf-8')

            response = lambda_client.invoke(
                FunctionName=arn_device_put_endpoint,
                InvocationType="RequestResponse",
                Payload=arg)

            data = response["Payload"].read().decode()

            res = json.loads(data)

            if res == "ok":
                return respond("200", dvc.serialize())
            else:
                return respond("400", event["device"])
    except:
        return respond("400", event["device"])
