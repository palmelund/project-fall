from server.respond import respond
from model import user


def lambda_handler(event, context):

    contacts = user.Contact.get_all()
    return_string = "["

    if not contacts:
        return respond("400", user.User(-1, "", "", "userAdmin").serialize())
    else:
        for ctc in contacts:
            return_string += ctc.serialize() + ","

        return_string = return_string[:-1] + "]"

        return respond("200", return_string)
