import psycopg2
import json
from database.connect_str import connect_str
from respond import respond
from model.alarm import *
from model.contact import *


def lambda_handler(event, context):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    response = event["response"]
    contact = json.loads(event["contact"])
    alarm = json.loads(event["alarm"])

    if response == 1:
        cursor.execute("UPDATE alarm SET status = -1, responder = " + contact.id + " WHERE id = " + alarm.id + "")
    else:
        cursor.execute("UPDATE alarm SET status = status + 1 WHERE id = " + alarm.id + ";")

    conn.commit()
    cursor.close()
    conn.close()
