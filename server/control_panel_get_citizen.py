from model import user
from respond import respond, build_response

def lambda_handler(event, context):
    if not event['citizenid']:
        return build_response("400", "Missing argument")

    return respond(None, user.User.get(event['citizenid']))
