import boto3
#from sns_credentials import region_name, aws_access_key_id, aws_secret_access_key, arn_endpoint
from sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key, arn_endpoint

# Get connection
sns_client = boto3.client(
    'sns',
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)


def create_endpoint(token):
    return sns_client.create_platform_endpoint(
        PlatformApplicationArn=arn_endpoint,
        Token=token
)


def update_endpoint(endpoint_arn, new_token):
    # TODO: This is untested
    return sns_client.set_endpoint_attributes(
        EndpointArn=endpoint_arn,
        Token=new_token
    )


def push_message(endpoint_arn, message):
    return sns_client.publish(
        PlatformApplicationArn=endpoint_arn,
        MessageStructure='string',
        Message=message
    )
