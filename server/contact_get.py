from server.respond import respond
from model import user


def lambda_handler(event, context):
    try:
        id = event["id"]
    except:
        return respond("400", user.User(-1, "", "", ""))

    if not id:
        return respond("400", user.User(-1, "", "", ""))

    usr = user.Contact.get(id)

    if not usr or usr.id == -1:
        return respond("400", user.User(-1, "", "", ""))
    else:
        return respond("200", usr.serialize())
