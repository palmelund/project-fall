from server.respond import respond
from model import user
import jwt

def lambda_handler(event, context):
    try:
        email = event['email']
        password = event['password']
    except:
        return respond("400", user.User(-1, "", "", "userAdmin").serialize())

    if not all(x is not None for x in [email, password]):
        return respond("400", user.User(-1, "", "", "userAdmin").serialize())

    usr = user.User.attempt_login(email, password)

    if not usr or usr.id == -1:
        return respond("400", user.User(-1, "", "", "userAdmin").serialize())
    else:
        usr.token = get_auth_token(usr)
        return respond("200", usr.serialize())


def get_auth_token(user):
    return jwt.encode({'user_id': user.id, 'user_role': user.role}, 'power123')
