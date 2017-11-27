from connect_str import connect_str
from model.user import *
import psycopg2


def get_all_citizens():
    allCitizens = ()

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, address, city, postnr FROM users, citizen WHERE user.id = citizen.userID")
    citizensRaw = cursor.fetchall()

    for citizen in citizensRaw:
        contacts = get_citizen_contacts()
        devices = get_user_devices(citizen[0])
        allCitizens.append(Citizen(citizen[0], citizen[1], citizen[2], contacts, devices, citizen[3], citizen[4], citizen[5]))


def get_citizen_contacts(citizenID):
    contacts = ()

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT users.id, users.name, user.email, contact.phone FROM users, contact, associateswith WHERE user.id = contact.userID AND associateswith.citizenID = %s AND associateswith.contactID = users.id", citizenID)
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
