from usermanager import add_user
from respond import build_response_no_ser


def lambda_handler(event, context):
    try:
        email = event['email']
        password = event['password']
        name = event['name']
        role = event['role']
    except Exception as ex:
        return build_response_no_ser("400", "Missing arguments!")

    if all(x is not None for x in [email, password, name, role]):
        return build_response_no_ser("400", "Missing arguments!")

    user = add_user(email, password, name, role)

    # TODO: Fix me
    if not user:
        return "Error: Could not create user"
    else:
        return user

