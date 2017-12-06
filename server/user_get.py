from server.respond import respond
from model import user

def lambda_handler(event, context):
    try:
        email = event['email']
        password = event['password']
    except:
        return respond("400", "Invalid email or password")

    if not all(x is not None for x in [email, password]):
        return respond("400", "Invalid email or password")

    usr = user.User.attempt_login(email, password)

    if not usr or usr.id == -1:
        return respond("400", "Invalid email or password")
    else:
        return respond("200", usr.serialize())