from connect_str import connect_str
from model.user import *
import psycopg2


def get_alarm(citizenID):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT alarm.status, alarm.responder FROM alarm WHERE activatedby = %s", citizenID)
    alarm = cursor.fetchone()

    return Alarm(alarm[0], get_citizen(citizenID), get_contact(alarm[1]))


def get_device(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT users.id, users.name, user.email FROM users WHERE users.id = %s", id)
    caRaw = cursor.fetchone()

    return UserAdmin(caRaw[0], caRaw[1], caRaw[2], caRaw[3])


def get_user(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE users.id = %s", id)
    userType = cursor.fetchone()

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

    cursor.execute("SELECT users.id, users.name, user.email FROM users WHERE users.id = %s", id)
    caRaw = cursor.fetchone()

    return UserAdmin(caRaw[0], caRaw[1], caRaw[2], caRaw[3])


def get_citizen_admin(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT users.id, users.name, user.email FROM users WHERE users.id = %s", id)
    caRaw = cursor.fetchone()

    citizens = get_citizen_admins_citizens(id)

    return CitizenAdmin(caRaw[0], caRaw[1], caRaw[2], caRaw[3], citizens)


def get_citizen_admins_citizens(admin_id):
    citizens = ()

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, address, city, postnr FROM users, citizen, manages WHERE users.id = citizen.userID AND manages.citizenid = users.id AND manages.adminid = %s", admin_id)
    citizensRaw = cursor.fetchall()

    for citizen in citizensRaw:
        contacts = get_citizen_contacts(citizen[0])
        devices = get_user_devices(citizen[0])
        citizens.append(Citizen(citizen[0], citizen[1], citizen[2], contacts, devices, citizen[3], citizen[4], citizen[5]))

    return citizens


def get_contact(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT users.id, users.name, user.email, contact.phone FROM users, contact WHERE users.id = contact.userID AND users.id = %s", id)
    contactRaw = cursor.fetchone()

    devices = get_user_devices(contactRaw[0])

    return Contact(contactRaw[0], contactRaw[1], contactRaw[2], contactRaw[4], devices)


def get_citizen(id):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, address, city, postnr FROM users, citizen WHERE users.id = citizen.userID AND user.id = %s", id)
    citizenRaw = cursor.fetchall()

    contacts = get_citizen_contacts(citizenRaw[0])
    devices = get_user_devices(citizenRaw[0])

    return Citizen(citizenRaw[0], citizenRaw[1], citizenRaw[2], contacts, devices, citizenRaw[3], citizenRaw[4], citizenRaw[5])


def get_all_citizens():
    allCitizens = ()

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, address, city, postnr FROM users, citizen WHERE users.id = citizen.userID")
    citizensRaw = cursor.fetchall()

    for citizen in citizensRaw:
        contacts = get_citizen_contacts(citizen[0])
        devices = get_user_devices(citizen[0])
        allCitizens.append(Citizen(citizen[0], citizen[1], citizen[2], contacts, devices, citizen[3], citizen[4], citizen[5]))

    return allCitizens


def get_citizen_contacts(citizenID):
    contacts = ()

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT users.id, users.name, user.email, contact.phone FROM users, contact, associateswith WHERE users.id = contact.userID AND associateswith.citizenID = %s AND associateswith.contactID = users.id", citizenID)
    contactsRaw = cursor.fetchall()

    for contact in contactsRaw:
        devices = get_user_devices(contact[0])

        contacts.append(Contact(contact[0], contact[1], contact[2], contact[4], devices))

    return contacts


def get_user_devices(userID):
    devices = ()

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT device.id, device.type FROM device, hasa WHERE device.id = hasa.deviceID AND hasa.userID = %s", userID)
    devicesRaw = cursor.fetchall()

    for device in devicesRaw:
        devices.append(Device(device[0], device[1]))

    return devices
