from model import user
from server.respond import respond


def lambda_handler(event, context):
    try:
        id = event["id"]
    except:
        return respond("400", user.User(-1, "", "", "").serialize())

    if not id:
        return respond("400", user.User(-1, "", "", "").serialize())

    ctz = user.Citizen.get(id)

    if not ctz or ctz.id == -1:
        return respond("400", user.User(-1, "", "", "").serialize())
    else:
        return respond("200", ctz.serialize())
