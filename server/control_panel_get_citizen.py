from model import user
from respond import respond, build_response, build_response_no_ser
import json

def lambda_handler(event, context):
    if not event['citizenid']:
        return build_response("400", "Missing argument")

    dump = json.dumps(user.User.get(event['citizenid']), default=lambda o: o.__dict__)
    print(json.loads(dump))
    return build_response_no_ser("200", json.dumps(user.User.get(event['citizenid']), default=lambda o: o.__dict__))
