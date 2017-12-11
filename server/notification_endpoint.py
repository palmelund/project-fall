from model import device
from server.respond import respond
from server.sns.sns_interface import create_endpoint, update_endpoint


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
