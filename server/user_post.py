from server.respond import respond
from model import user


def lambda_handler(event, context):
    try:
        usr = user.deserialize(event["user"])
        password = event["password"]
    except:
        return respond("400", user.User(-1, "", "", "").serialize())

    if not all(x is not None for x in [usr, password]):
        return respond("400", user.User(-1, "", "", "").serialize())

    try:
        if usr.role == "citizen":
            return respond("200", user.User.create_new_user(usr.name, usr.email, password, usr.role, usr.address, usr.city, usr.postnr).serialize())
        elif usr.role == "contact":
            return respond("200", user.User.create_new_user(usr.name, usr.email, password, usr.role).serialize())
        elif usr.role == "citizenAdmin":
            return respond("200", user.User.create_new_user(usr.name, usr.email, password, usr.role).serialize())
        elif usr.role == "userAdmin":
            return respond("200", user.User.create_new_user(usr.name, usr.email, password, usr.role).serialize())
        else:
            return respond("400", user.User(-1, "", "", "").serialize())
    except:
        return respond("400", user.User(-1, "", "", "").serialize())
