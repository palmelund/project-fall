from model import user
from server.respond import respond

def lambda_handler(event, context):
    try:
        usr = usr = user.deserialize(str(event["user"]))
    except:
        return respond("400", event["user"])

    if not user:
        return respond("400", event["user"])

    try:
        usr.delete()
        return respond("200", user.User(-1, "", "", usr.role).serialize())
    except:
        return respond("400", event["user"])