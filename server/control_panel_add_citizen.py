import psycopg2
import model
from model import citizen
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

    # Create an alarm
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM citizenadmin WHERE userid = %s", event['adminid'])
    admin = cursor.fetchone()

    if not admin:
        return build_response("400", "Not admin")

    user = add_user(username, email, password, name, 'citizen')
    cursor.execute("INSERT INTO citizen VALUES (%s, %s, %s, %s, %s)", (user.id, address, city, postal, admin[0]))
    citizen = cursor.fetchone()

    citizenuser = model.citizen.Citizen(user.id, user.name, user.email, user.username, None, None, None)

    return respond(None, citizenuser)
