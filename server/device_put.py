from model.device import deserialize
from server.respond import respond


def lambda_handler(event, context):
    try:
        dvc = deserialize(event["device"])
    except:
        return respond("400", event["device"])

    if not dvc:
        return respond("400", event["device"])

    dvc.put()

    return respond("200", dvc.serialize())
