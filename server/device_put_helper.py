from model import device


def lambda_handler(event, context):
    dvc = device.deserialize(event["device"])
    dvc.put()

    return "ok"
