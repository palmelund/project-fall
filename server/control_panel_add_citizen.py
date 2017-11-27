import psycopg2
import model
from connect_str import connect_str
from usermanager import add_user
from respond import respond, build_response
from model import user

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

    citizen = user.Citizen()

    print(adminid)

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    admin = user.User.get(adminid);
    if type(admin) != user.CitizenAdmin:
        return build_response("400", "Not admin")

    usr = add_usr(usrname, email, password, name, 'citizen')

    if not usr:
        return build_response("400", "Could not add usr")

    cursor.execute("INSERT INTO citizen VALUES (%s, %s, %s, %s, %s)", (usr[0], address, city, postal, adminid))

    citizenuser = model.user.Citizen(usr[0], usr[4], usr[5], usr[1], None, None, None)

    return respond(None, citizenuser.__dict__)
