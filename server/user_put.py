from model.user import deserialize
from server.respond import respond


def lambda_handler(event, context):
    try:
        usr = deserialize(event["user"])
    except:
        return respond("400", event["user"])

    if not usr:
        return respond("400", event["user"])

    usr.update()

    return respond("200", usr.serialize())
