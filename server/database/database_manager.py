import hashlib
import json
import uuid

import psycopg2
from model import alarm, device, user
from server.database.connect_str import connect_str


def set_alarm(alm):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    # If an old alarm still remains in the system, delete it
    cursor.execute("DELETE FROM alarm WHERE activatedby = %s", [alm.activatedby.id])

    # To avoid null error
    if not alm.responder:
        resp = None
    else:
        resp = alm.responder.id

    cursor.execute("INSERT INTO alarm VALUES (%s, %s, %s) RETURNING activatedby",
                   [alm.status, alm.activatedby.id, resp])
    uid = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return alarm.Alarm.get(uid)


def get_alarm(citizen_id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT alarm.status, alarm.responder FROM alarm WHERE activatedby = %s", [citizen_id])
    alm = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return alarm.Alarm(alm[0], get_citizen(citizen_id), get_contact(alm[1]))


def delete_alarm(citizen_id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM alarm WHERE activatedby = %s", [citizen_id])

    conn.commit()
    cursor.close()
    conn.close()


def update_device(dvc):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    if dvc.devicetype == "appdevice":
        content = {"token": dvc.token, "arn": dvc.arn}
    elif dvc.devicetype == "alexadevice":
        content = {"user_id": dvc.user_id}
    elif dvc.devicetype == "iftttdevice":
        content = {"token": dvc.token}
    elif dvc.devicetype == "smsdevice":
        content = {"phone_number": dvc.phone_number}
    elif dvc.devicetype == "phonecalldevice":
        content = {"phone_number": dvc.phone_number}
    else:
        content = {}

    cursor.execute("UPDATE device SET content = %s WHERE id = %s", [json.dumps(content), dvc.id])

    conn.commit()
    cursor.close()
    conn.close()


def get_device_from_user_id(user_id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT device.id FROM device, devicemap WHERE devicemap.token = %s AND devicemap.deviceid = device.id", [user_id])
    dvc = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return device.AlexaDevice(dvc[0], user_id)


def get_device(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT device.id, device.devicetype, device.content FROM device WHERE id = %s",
                   [id])
    dvc = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return tuple_to_device(dvc)


def get_device_owner(deviceid):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT userid FROM hasa WHERE deviceid = %s", [deviceid])
    uid = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return get_user(uid)


def post_device(dvc, usr):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    content = pack_content(dvc)

    cursor.execute("INSERT INTO device VALUES (DEFAULT, %s, %s) RETURNING id", [content, dvc.devicetype])
    device_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO hasa VALUES (%s, %s)", [usr.id, device_id])

    if dvc.devicetype == "alexadevice":
        cursor.execute("INSERT INTO devicemap VALUES (%s, %s)", [dvc.user_id, dvc.id])

    conn.commit()
    cursor.close()
    conn.close()


def get_user(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE users.id = %s", [id])
    user_type = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    if user_type == "citizen":
        return get_citizen(id)
    elif user_type == "contact":
        return get_contact(id)
    elif user_type == "citizenAdmin":
        return get_citizen_admin(id)
    elif user_type == "userAdmin":
        return get_user_admin(id)


def get_user_admin(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT users.id, users.name, users.email FROM users WHERE users.id = %s", [id])
    ua = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return user.UserAdmin(ua[0], ua[1], ua[2])


def get_citizen_admin(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT users.id, users.name, users.email FROM users WHERE users.id = %s", [id])
    ca = cursor.fetchone()

    citizens = get_citizen_admins_citizens(id)

    conn.commit()
    cursor.close()
    conn.close()

    return user.CitizenAdmin(ca[0], ca[1], ca[2], citizens)


def get_citizen_admins_citizens(admin_id):
    citizens = []

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email, address, city, postnr FROM users, citizen, manages WHERE users.id = citizen.userID AND manages.citizenid = users.id AND manages.adminid = %s",
        [admin_id])
    ctz = cursor.fetchall()

    for citizen in ctz:
        contacts = get_citizen_contacts(citizen[0])
        devices = get_user_devices(citizen[0])
        citizens.append(
            user.Citizen(citizen[0], citizen[1], citizen[2], contacts, devices, citizen[3], citizen[4],
                         citizen[5]))

    conn.commit()
    cursor.close()
    conn.close()

    return citizens


def get_contact(id):
    if not id:
        return None

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT users.id, users.name, users.email FROM users, contact WHERE users.id = contact.userID AND users.id = %s",
        [id])
    ctc = cursor.fetchone()

    devices = get_user_devices(ctc[0])

    conn.commit()
    cursor.close()
    conn.close()

    return user.Contact(ctc[0], ctc[1], ctc[2], devices)


def get_contact_all():
    all_contacts = []

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT users.id, users.name, users.email FROM users, contact WHERE users.id = contact.userID")
    citizens_raw = cursor.fetchall()

    for ctc in citizens_raw:
        devices = get_user_devices(ctc[0])
        all_contacts.append(user.Contact(ctc[0], ctc[1], ctc[2], devices))

    conn.commit()
    cursor.close()
    conn.close()

    return all_contacts


def get_citizen(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email, address, city, postnr FROM users, citizen WHERE users.id = citizen.userID AND users.id = %s",
        [id])
    ctz = cursor.fetchone()

    contacts = get_citizen_contacts(ctz[0])
    devices = get_user_devices(ctz[0])

    conn.commit()
    cursor.close()
    conn.close()

    return user.Citizen(ctz[0], ctz[1], ctz[2], contacts, devices, ctz[3], ctz[4], ctz[5])


def get_all_citizens():
    allCitizens = []

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email, address, city, postnr FROM users, citizen WHERE users.id = citizen.userID")
    ctzs = cursor.fetchall()

    for ctz in ctzs:
        contacts = get_citizen_contacts(ctz[0])
        devices = get_user_devices(ctz[0])

        allCitizens.append(user.Citizen(ctz[0], ctz[1], ctz[2], contacts, devices, ctz[3], ctz[4], ctz[5]))

    conn.commit()
    cursor.close()
    conn.close()

    return allCitizens


def get_citizen_contacts(citizen_id):
    contacts = []

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT users.id, users.name, users.email FROM users, contact, associateswith WHERE users.id = contact.userID AND associateswith.citizenID = %s AND associateswith.contactID = users.id",
        [citizen_id])
    ctc = cursor.fetchall()

    for contact in ctc:
        devices = get_user_devices(contact[0])

        contacts.append(user.Contact(contact[0], contact[1], contact[2], devices))

    conn.commit()
    cursor.close()
    conn.close()

    return contacts


def get_user_devices(user_id):
    devices = []

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT device.id, device.devicetype, device.content FROM device, hasa WHERE device.id = hasa.deviceID AND hasa.userID = %s",
        [user_id])
    dvcs = cursor.fetchall()

    for dvc in dvcs:
        devices.append(tuple_to_device(dvc))

    conn.commit()
    cursor.close()
    conn.close()

    return devices


def add_user(email, password, name, role):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    salt = get_salt()
    hashed_password = hash_password(password, salt)

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", [email])
        exist = cursor.fetchone()

        # if exist:
            # return None

        cursor.execute("INSERT INTO users VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING id, name, email, role;",
                       (hashed_password, salt, name, email, role))
        usr = cursor.fetchone()

    except Exception as ex:
        return ex

    conn.commit()
    cursor.close()
    conn.close()

    return user.User(usr[0], usr[1], usr[2], usr[3])


def add_citizen(user_id, address, city, postnr, managedby):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO citizen VALUES (%s, %s, %s, %s, %s)", (user_id, address, city, postnr, managedby))

    conn.commit()
    cursor.close()
    conn.close()

    return get_citizen(user_id)


def add_contact(userid):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO contact VALUES (%s)", [userid])

    conn.commit()
    cursor.close()
    conn.close()

    return get_contact(userid)


def add_citizen_admin(userid):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO citizenadmin VALUES (%s)", [userid])

    conn.commit()
    cursor.close()
    conn.close()

    return get_citizen_admin(userid)


def add_user_admin(userid):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO useradmin VALUES (%s)", [userid])

    conn.commit()
    cursor.close()
    conn.close()

    return get_user_admin(userid)


def update_citizen_admin(citizen_admin_id, added_citizens, removed_citizens):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    for ctz in added_citizens:
        cursor.execute("INSERT INTO manages VALUES (%s, %s)", [citizen_admin_id, ctz.id])

    for ctz in removed_citizens:
        cursor.execute("DELETE FROM manages WHERE adminid = %s AND citizenid = %s", [[citizen_admin_id, ctz.id]])

    conn.commit()
    cursor.close()
    conn.close()


def update_contact(contact_id, added_devices, removed_devices):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    for dvc in added_devices:
        cursor.execute("INSERT INTO hasa VALUES (%s, %s)", [contact_id, dvc.id])

    for dvc in removed_devices:
        cursor.execute("DELETE FROM hasa WHERE userid = %s AND deviceid = %s", [contact_id, dvc.id])

    conn.commit()
    cursor.close()
    conn.close()


def update_citizen(ctz, added_devices, removed_devices, added_contacts, removed_contacts):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    for dvc in added_devices:
        cursor.execute("INSERT INTO hasa VALUES (%s, %s)", [ctz.id, dvc.id])

    for dvc in removed_devices:
        cursor.execute("DELETE FROM hasa WHERE userid = %s AND deviceid = %s", [ctz.id, dvc.id])

    for ctc in added_contacts:
        cursor.execute("INSERT INTO associateswith VALUES (%s, %s)", [ctz.id, ctc.id])

    for ctc in removed_contacts:
        cursor.execute("DELETE FROM associateswith VALUES (%s, %s)", [ctz.id, ctc.id])

    cursor.execute("UPDATE citizen SET address = %s, city = %s, postnr = %s WHERE userid = %s;", [ctz.address, ctz.city, ctz.postnr, ctz.id])

    conn.commit()
    cursor.close()
    conn.close()


def update_user(usr):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET email = %s WHERE id = %s", [usr.email, usr.id])

    conn.commit()
    cursor.close()
    conn.close()


def delete_user(user_id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = %s", [user_id])

    conn.commit()
    cursor.close()
    conn.close()


def delete_citizen(user_id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM associateswith WHERE citizenid = %s", [user_id])
    cursor.execute("DELETE FROM citizen WHERE userid = %s", [user_id])

    cursor.execute("SELECT deviceid FROM hasa WHERE userid = %s", [user_id])
    dvcs = cursor.fetchall()

    for dvc in dvcs:
        cursor.execute("DELETE FROM device WHERE id = %s", [dvc])

    cursor.execute("DELETE FROM hasa WHERE userid = %s", [user_id])

    cursor.execute("DELETE FROM users WHERE id = %s", [user_id])

    conn.commit()
    cursor.close()
    conn.close()


def delete_contact(user_id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM contact WHERE userid = %s", [user_id])
    cursor.execute("DELETE FROM associateswith WHERE contactid = %s", [user_id])

    cursor.execute("SELECT deviceid FROM hasa WHERE userid = %s", [user_id])
    dvcs = cursor.fetchall()

    for dvc in dvcs:
        cursor.execute("DELETE FROM device WHERE id = %s", [dvc])

    cursor.execute("DELETE FROM hasa WHERE userid = %s", [user_id])

    cursor.execute("DELETE FROM users WHERE id = %s", [user_id])

    conn.commit()
    cursor.close()
    conn.close()


def delete_user_admin(user_id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM useradmin WHERE id = %s", [user_id])

    cursor.execute("DELETE FROM users WHERE id = %s", [user_id])

    conn.commit()
    cursor.close()
    conn.close()


def delete_citizen_admin(user_id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM citizenadmin WHERE userid = %s", [user_id])

    cursor.execute("DELETE FROM manages WHERE adminid = %s", [user_id])

    cursor.execute("DELETE FROM users WHERE id = %s", [user_id])

    conn.commit()
    cursor.close()
    conn.close()


def delete_device(device_id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM hasa WHERE deviceid = %s", [device_id])

    cursor.execute("DELETE FROM device WHERE id = %s", [device_id])

    conn.commit()
    cursor.close()
    conn.close()


def associate(citizen_id, contact_id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO associateswith VALUES (%s, %s);", (citizen_id, contact_id))

    conn.commit()
    cursor.close()
    conn.close()


def hasa(user_id, device_id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO hasa VALUES (%s, %s);", (user_id, device_id))

    conn.commit()
    cursor.close()
    conn.close()


def login(email, password):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT id, password, salt FROM users WHERE email = %s", [email])
    usr = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not usr:
        return None

    if check_password(password, usr[1], usr[2]):
        return get_user(usr[0])
    else:
        return user.User(-1, "", "", "")


def get_salt():
    return uuid.uuid4().hex


def hash_password(password, salt):
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


def check_password(password, hashed_password, salt):
    return hashed_password == hash_password(password, salt)


def truncate_all_tables():
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE alarm, associateswith, citizen, citizenadmin, contact, device, devicemap, hasa, manages, useradmin, users;")

    conn.commit()
    cursor.close()
    conn.close()


def pack_content(dvc):
    if dvc.devicetype == "appdevice":
        return json.dumps({"token": dvc.token, "arn": dvc.arn})
    elif dvc.devicetype == "alexadevice":
        return json.dumps({"user_id": dvc.user_id})
    elif dvc.devicetype == "iftttdevice":
        return json.dumps({"token": dvc.token})
    elif dvc.devicetype == "smsdevice":
        return json.dumps({"phone_number": dvc.phone_number})
    elif dvc.devicetype == "phonecalldevice":
        return json.dumps({"phone_number": dvc.phone_number})
    else:
        raise Exception


def tuple_to_device(dvc):
    device_type = dvc[1]
    content = json.loads(dvc[2])

    if device_type == "appdevice":
        return device.AppDevice(dvc[0], content["token"], content["arn"])
    elif device_type == "alexadevice":
        return device.AlexaDevice(dvc[0], content["user_id"])
    elif device_type == "iftttdevice":
        return device.IFTTTDevice(dvc[0], content["token"])
    elif device_type == "smsdevice":
        return device.SmsDevice(dvc[0], content["phone_number"])
    elif device_type == "phonecalldevice":
        return device.PhoneCallDevice(dvc[0], content["phone_number"])
    else:
        raise Exception
