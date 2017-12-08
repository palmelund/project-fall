from server.respond import respond
from model import user
import json
import jwt


def lambda_handler(event, context):
    try:
        usr = user.deserialize(event["user"])
        #usr = user.deserialize(event["user"])
        password = event["password"]
    except:
        return respond("400", user.User(-1, "", "", "").serialize())

    if not all(x is not None for x in [usr, password]):
        return respond("400", user.User(-1, "", "", "").serialize())

    try:
        if usr.role == "citizen":
            _usr = user.User.create_new_user(usr.name, usr.email, password, usr.role, usr.address, usr.city, usr.postnr)
            _usr.token = get_auth_token(_usr)
            return respond("200", _usr.serialize())
        else:
            _usr = user.User.create_new_user(usr.name, usr.email, password, usr.role)
            _usr.token = get_auth_token(_usr)
            return respond("200", _usr.serialize())

    except Exception as ex:
        raise ex
        return respond("400", user.User(-1, "", "", "").serialize())

def get_auth_token(user):
    return jwt.encode({'user_id': user.id, 'user_role': user.role}, 'power123')
