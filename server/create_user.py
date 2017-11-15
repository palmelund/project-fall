from usermanager import add_user


def lambda_handler(event, context):
    username = event['username']
    email = event['email']
    password = event['password']
    name = event['name']
    role = event['role']

    user = add_user(username, email, password, name, role)

    if not user:
        return "Error: Could not create user"
    else:
        return user

