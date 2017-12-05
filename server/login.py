from respond import respond, build_response, build_response_no_ser
from model.user import User
import json
from json_serializer import JsonSerializer


def lambda_handler(event, context):
    try:
        email = event['email']
        password = event['password']
    except:
        return build_response("400", {"id": -1})

    if not all(x is not None for x in [email, password]):
        return build_response("400", {"id": -1})

    usr = User.attempt_login(email, password)  # login(email, password)

    if not usr:
        return build_response("400", {"id": -1})
    else:
        return build_response_no_ser("200", json.dumps(User.get(usr[0]).working_serializer(), cls=JsonSerializer))
        # return build_response_no_ser("200",       {"id": user[0], "email": user[4], "name": user[3], "role": user[5]})
