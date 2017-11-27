from connect_str import connect_str
from respond import build_response_no_par
from model.user import *
import psycopg2
import json


def get_all_citizens():
    allCitizens = ()

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users, citizen WHERE users.id = citizen.userID")
    citizensRaw = cursor.fetchall()

    for citizen in citizensRaw:
        print(citizen)


# TODO: What if contact has multiple citizens, and uses the same phone number?
def get_contact_from_number(number):
    if not number:
        return ()

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contact WHERE phone = %s", [number])
    contact = cursor.fetchfirst()

    conn.commit()
    cursor.close()
    conn.close()

    if not contact:
        return build_response_no_par(400, {"id": -1})

    #TODO: Return contact
