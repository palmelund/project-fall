import boto3
from sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key, arn_endpoint
import json
from pprint import pprint


def create_endpoint(token):
    # Get connection
    sns_client = boto3.client(
        'sns',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    return sns_client.create_platform_endpoint(
        PlatformApplicationArn=arn_endpoint,
        Token=token
)


def update_endpoint(endpoint_arn, new_token):
    # Get connection
    sns_client = boto3.client(
        'sns',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # TODO: This is untested
    return sns_client.set_endpoint_attributes(
        EndpointArn=endpoint_arn,
        Token=new_token
    )


def push_message(endpoint_arn, message):
    # Get connection
    sns_client = boto3.client(
        'sns',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    return sns_client.publish(
        PlatformApplicationArn=endpoint_arn,
        MessageStructure='string',
        Message=message
    )


def send_sms(number, message):
    print("Sending SMS")
    print(number)
    print(message)

    # Get connection
    sns_client = boto3.client(
        'sns',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    print(region_name)
    print(aws_access_key_id)
    print(aws_secret_access_key)

    res = sns_client.publish(
        PhoneNumber=str(number),
        Message=str(message)
    )
    print(res)
    return res


def push_all(contacts, message):
    print("push all")
    for c in contacts:
        pprint(c.serialize())
        for d in c.devices:
            print("Device")
            pprint(d.serialize())
            content = json.loads(d.content)
            if content["messagetype"] == "notification":
                if content["type"] == "android":
                    print("Arn: " + content["arn"])
                    print("Message: " + message)
                    push_message(content["arn"], message)


def send_all(contacts, message):
    print("send all")
    for c in contacts:
        pprint(c.serialize())
        number = ""
        for d in c.devices:
            print("Device")
            pprint(d.serialize())
            content = json.loads(d.content)
            if content["messagetype"] == "sms":
                print(c.phone)
                number = c.phone
        if number:
            send_sms(number, message)
        else:
            print("???")
