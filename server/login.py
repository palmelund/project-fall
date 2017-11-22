from usermanager import login
from respond import respond


def lambda_handler(event, context):
    user = login(event['email'], event['password'])

    if not user:
        return respond(None, {"id": -1 })
    else:
        return respond(None, {"id": user[0]})