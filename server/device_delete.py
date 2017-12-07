from model.device import deserialize
from server.respond import respond
from model import device


def lambda_handler(event, context):
    try:
        dvc = deserialize(event["device"])
    except:
        return respond("400", event["device"])

    if not dvc:
        dvc = deserialize(event["device"])

    dvc.delete()

    return respond("200", device.Device(-1, "", "", "").serialize())
