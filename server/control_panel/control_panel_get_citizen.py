from model import user
from respond import respond, build_response, build_response_no_ser
import json


def lambda_handler(event, context):
    if not event['citizenid']:
        return build_response("400", "Missing argument")

    return build_response_no_ser("200", user.User.get(event['citizenid']).serialize())