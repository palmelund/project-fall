import boto3
from server.sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key
from server.endpoints import arn_sns_android_endpoint


def create_endpoint(token):
    # Get connection
    sns_client = boto3.client(
        'sns',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    return sns_client.create_platform_endpoint(
        PlatformApplicationArn=arn_sns_android_endpoint,
        Token=token
    )["ArnEndpoint"]


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
        EndpointArn=arn_sns_android_endpoint,
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
        PlatformApplicationArn=arn_sns_android_endpoint,
        MessageStructure='string',
        Message=message
    )


# def send_sms(number, message):
#     print("Sending SMS")
#     print(number)
#     print(message)
#
#     # Get connection
#     sns_client = boto3.client(
#         'sns',
#         region_name=region_name,
#         aws_access_key_id=aws_access_key_id,
#         aws_secret_access_key=aws_secret_access_key
#     )
#
#     return
#
#     return sns_client.publish(
#         PhoneNumber=str(number),
#         Message=str(message)
#     )
