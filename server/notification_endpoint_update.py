from model.user import Citizen
from model import user
from model import device
from server.sns.sns_interface import update_endpoint
import json
import boto3
from server.endpoints import arn_notification_endpoint_store_endpoint
from server.respond import respond
from server.sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key


def lambda_handler(event, context):
    try:
        dvc_old: device.AppDevice = device.deserialize(event["old_device"])
        dvc_new: device.AppDevice = device.deserialize(event["new_device"])

    except Exception as ex:
        return respond("400", "error")

    lambda_client = boto3.client('lambda',
                                 region_name=region_name,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)

    if not dvc_old.arn or not dvc_new.arn or dvc_old.arn != dvc_new.arn:
        return respond("400", "error")
    if dvc_old.token == dvc_new.token:
        return respond("200", "ok")

    try:
        update_endpoint(dvc_new.arn, dvc_new.token)

        arg = bytes(json.dumps({"action": "update", "device": dvc_new.serialize()}), 'utf-8')

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
    except:
        return respond("400", "")


    # try:
    #     for dvc in usr.devices:
    #         content = device.deserialize(dvc)
    #         if content["devicetype"] == "smartphone" and content["messagetype"] == "notification" and content["token"] == oldtoken:
    #             content["token"] = newtoken
    #
    #             update_endpoint(content["arn"], newtoken)
    #
    #             dump = json.dumps({"messagetype": "notification", "token": newtoken, "arn": content["arn"], "action": "create"})
    #             arg = bytes(json.dumps({"citizen": dump}), 'utf-8')
    #
    #             response = lambda_client.invoke(
    #                 FunctionName=arn_notification_endpoint_store_endpoint,
    #                 InvocationType="RequestResponse",
    #                 Payload=arg)
    #
    #             data = response["Payload"].read().decode()
    #             res = json.loads(data)
    #
    #             if res["status"] == "ok":
    #                 return build_response_no_ser("200", "ok")
    #             else:
    #                 return build_response_no_ser("400", "error")
    # except Exception as ex:
    #     return ex