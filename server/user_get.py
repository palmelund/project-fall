from server.respond import respond
from model import user


def lambda_handler(event, context):
    try:
        email = event['email']
        password = event['password']
    except:
        return respond("400", user.User(-1, "", "", ""))

    if not all(x is not None for x in [email, password]):
        return respond("400", user.User(-1, "", "", ""))

    usr = user.User.attempt_login(email, password)

    if not usr or usr.id == -1:
        return respond("400", user.User(-1, "", "", ""))
    else:
        return respond("200", usr.serialize())
