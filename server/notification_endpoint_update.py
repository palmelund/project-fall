import requests

def lambda_handler(event, context):
    try:
        ctz: Citizen = user.deserialize(json.loads(event["citizen"]))
        token = event["token"]

    except Exception as ex:
        return build_response_no_ser("400", {"status": "error"})

    lambda_client = boto3.client('lambda',
                                 region_name=region_name,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)

    try: