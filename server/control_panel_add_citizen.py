import psycopg2
import model
from connect_str import connect_str
from usermanager import add_user
from respond import respond, build_response


def lambda_handler(event, context):
    try:
        adminid = event['adminid']
        username = event['username']
        password = event['password']
        name = event['name']
        email = event['email']
        address = event['city']
        city = event['city']
        postal = event['postal']
    except Exception as ex:
        print(ex)
        return build_response("400", "missing arguments")
        # TODO

    if all(x is not None for x in [adminid, username, password, name, email, address, city, postal]):
        return build_response("400", "missing arguments")

    print(adminid)

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM citizenadmin WHERE userid = %s", [adminid])
    admin = cursor.fetchone()

    if not admin:
        return build_response("400", "Not admin")

    user = add_user(username, email, password, name, 'citizen')

    if not user:
        return build_response("400", "Could not add user")

    cursor.execute("INSERT INTO citizen VALUES (%s, %s, %s, %s, %s)", (user[0], address, city, postal, adminid))

    citizenuser = model.user.Citizen(user[0], user[4], user[5], user[1], None, None, None)

    return respond(None, citizenuser.__dict__)
