import psycopg2
import json
from connect_str import connect_str
from respond import respond
from model.alarm import *
from model.contact import *


class ContactHelper:
    def __init__(self, j):
        self.id = 0
        self.name = ""
        self.email = ""
        self.username = ""
        self.phone = ""
        self.devices = ""
        self.__dict__ = json.loads(j)


class AlarmHelper:
    def __init__(self, j):
        self.id = 0
        self.status = 0
        self.citizen = 0
        self.__dict__ = json.loads(j)


def lambda_handler(event, context):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    response = event["response"]
    contact_info = ContactHelper(event["contact"])
    contact = Contact(contact_info.id, contact_info.name, contact_info.email, contact_info.username, contact_info.phone, contact_info.devices)  # json.loads(event["contact"])
    print(contact)
    alarm_info = AlarmHelper(event["alarm"])
    alarm = Alarm(alarm_info.id, alarm_info.citizen, alarm_info.status)
    print(alarm)

    if response == 1:
        cursor.execute("UPDATE alarm SET status = -1, responder = %s WHERE id = %s;", (contact.id, alarm.id))
        # cursor.execute("UPDATE alarm SET status = -1, responder = " + contact.id + " WHERE id = " + alarm.id + "")
    else:
        cursor.execute("UPDATE alarm SET status = status + 1 WHERE id = %s;", [alarm.id])
        # cursor.execute("UPDATE alarm SET status = status + 1 WHERE id = " + alarm.id + ";")

    conn.commit()
    cursor.close()
    conn.close()

    return respond(None, "")
