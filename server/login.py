from usermanager import login
from respond import respond, build_response, build_response_no_ser


def lambda_handler(event, context):
    try:
        email = event['email']
        password = event['password']
    except:
        return build_response(str(400), {"id": -1})

    user = login(email, password)

    if not user:
        return build_response(str(400), {"id": -1})
    else:
        return build_response_no_ser(str(200), {"id": user[0], "username": user[1], "email": user[5], "name": user[4], "role": user[6]})
