from server.respond import respond
from model import user


def lambda_handler(event, context):

    citizens = user.Citizen.get_all()
    return_string = "["

    if not citizens:
        return respond("400", user.User(-1, "", "", "userAdmin").serialize())
    else:
        for ctz in citizens:
            return_string += ctz.serialize() + ","

        return_string = return_string[:-1] + "]"

        return respond("200", return_string)
