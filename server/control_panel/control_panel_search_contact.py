from respond import build_response
from model import contact


def lambda_handler(event, context):
    try:
        number = event['number']
    except Exception as ex:
        print(ex)
        return build_response(400, "Missing arguments!")

    if not number:
        return build_response(400, "Missing arguments!")

    user = contact.get(number)

    if not user:
        # TODO: Return error
    else:
        # TODO: Return user