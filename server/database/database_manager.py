from connect_str import connect_str
from model.user import *
from model import alarm
from respond import respond
from model import user
import psycopg2
import hashlib
import uuid


def set_alarm(alm):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM alarm WHERE activatedby = %s", [alm.activatedby.id])

    if not alm.responder:
        resp = None
    else:
        resp = alm.responder.id

    cursor.execute("INSERT INTO alarm VALUES (%s, %s, %s)", [alm.status, alm.activatedby.id, resp])

    conn.commit()
    cursor.close()
    conn.close()

    return respond(None)


def get_alarm(citizenID):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT alarm.status, alarm.responder FROM alarm WHERE activatedby = %s", [citizenID])
    alm = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return alarm.Alarm(alm[0], get_citizen(citizenID), get_contact(alm[1]))


def get_device(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT users.id, users.name, users.email FROM users WHERE users.id = %s", id)
    caRaw = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return user.UserAdmin(caRaw[0], caRaw[1], caRaw[2], caRaw[3])


def get_user(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE users.id = %s", id)
    userType = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    if userType == "citizen":
        return get_citizen(id)
    elif userType == "contact":
        return get_citizen(id)
    elif userType == "CitizenAdmin":
        return get_citizen_admin(id)
    elif userType == "UserAdmin":
        return get_user_admin(id)


def get_user_admin(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT users.id, users.name, users.email FROM users WHERE users.id = %s", id)
    caRaw = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return user.UserAdmin(caRaw[0], caRaw[1], caRaw[2], caRaw[3])


def get_citizen_admin(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT users.id, users.name, users.email FROM users WHERE users.id = %s", id)
    caRaw = cursor.fetchone()

    citizens = get_citizen_admins_citizens(id)

    conn.commit()
    cursor.close()
    conn.close()

    return user.CitizenAdmin(caRaw[0], caRaw[1], caRaw[2], caRaw[3], citizens)


def get_citizen_admins_citizens(admin_id):
    citizens = []

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, address, city, postnr FROM users, citizen, manages WHERE users.id = citizen.userID AND manages.citizenid = users.id AND manages.adminid = %s", admin_id)
    citizensRaw = cursor.fetchall()

    for citizen in citizensRaw:
        contacts = get_citizen_contacts(citizen[0])
        devices = get_user_devices(citizen[0])
        citizens.append(user.Citizen(citizen[0], citizen[1], citizen[2], contacts, devices, citizen[3], citizen[4], citizen[5]))

    conn.commit()
    cursor.close()
    conn.close()

    return citizens


def get_contact(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT users.id, users.name, users.email, contact.phone FROM users, contact WHERE users.id = contact.userID AND users.id = %s", id)
    contactRaw = cursor.fetchone()

    devices = get_user_devices(contactRaw[0])

    conn.commit()
    cursor.close()
    conn.close()

    return user.Contact(contactRaw[0], contactRaw[1], contactRaw[2], contactRaw[4], devices)


def get_citizen(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, address, city, postnr FROM users, citizen WHERE users.id = citizen.userID AND users.id = %s", id)
    citizenRaw = cursor.fetchone()

    contacts = get_citizen_contacts(citizenRaw[0])
    devices = get_user_devices(citizenRaw[0])

    conn.commit()
    cursor.close()
    conn.close()

    return user.Citizen(citizenRaw[0], citizenRaw[1], citizenRaw[2], contacts, devices, citizenRaw[3], citizenRaw[4], citizenRaw[5])


def get_all_citizens():
    allCitizens = []

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, address, city, postnr FROM users, citizen WHERE users.id = citizen.userID")
    citizensRaw = cursor.fetchall()

    for citizen in citizensRaw:
        contacts = get_citizen_contacts(citizen[0])
        devices = get_user_devices(citizen[0])

        allCitizens.append(user.Citizen(citizen[0], citizen[1], citizen[2], contacts, devices, citizen[3], citizen[4], citizen[5]))

    conn.commit()
    cursor.close()
    conn.close()

    return allCitizens


def get_citizen_contacts(citizenID):
    contacts = []

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT users.id, users.name, users.email, contact.phone FROM users, contact, associateswith WHERE users.id = contact.userID AND associateswith.citizenID = %s AND associateswith.contactID = users.id", [citizenID])
    contactsRaw = cursor.fetchall()

    for contact in contactsRaw:
        devices = get_user_devices(contact[0])

        contacts.append(user.Contact(contact[0], contact[1], contact[2], contact[3], devices))

    conn.commit()
    cursor.close()
    conn.close()

    return contacts


def get_user_devices(userID):
    devices = []

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT device.id, device.type FROM device, hasa WHERE device.id = hasa.deviceID AND hasa.userID = %s", [userID])
    devicesRaw = cursor.fetchall()

    for device in devicesRaw:
        devices.append(Device(device[0], device[1]))

    conn.commit()
    cursor.close()
    conn.close()

    return devices


def add_user(username, email, password, name, role):
    # TODO: Avoid duplicate database entries
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    salt = get_salt()
    hashed_password = hash_password(password, salt)

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        exist = cursor.fetchone()

        if exist:
            return None

        cursor.execute("INSERT INTO users VALUES (DEFAULT, %s, %s, %s, %s, %s, %s);", (username, hashed_password, salt, name, email, role))
        cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cursor.fetchone()
    except Exception:
        return None

    conn.commit()
    cursor.close()
    conn.close()

    if not user:
        return None
    else:
        return get_user(user[0])


def add_citizen(userid, address, city, postnr, managedby):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO citizen VALUES (%s, %s, %s, %s, %s)", (userid, address, city, postnr, managedby))

    conn.commit()
    cursor.close()
    conn.close()

    return get_citizen(userid)


def add_citizen_admin(userid):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO citizenadmin VALUES (%s)", [userid])

    conn.commit()
    cursor.close()
    conn.close()

    return get_citizen_admin(userid)


def add_admin(userid):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    # TODO
    # cursor.execute("INSERT INTO ")

    conn.commit()
    cursor.close()
    conn.close()

    return get_user_admin(userid)


def login(email, password):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", [email])
    user = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not user:
        return None

    if check_password(password, user[2], user[3]):
        return user
    else:
        return None


def get_salt():
    return uuid.uuid4().hex


def hash_password(password, salt):
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


def check_password(password, hashed_password, salt):
    return hashed_password == hash_password(password, salt)
