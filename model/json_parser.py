import json
from model import alarm, citizen, citizen_admin, contact, device, settings, user, user_admin


def parse_alarm(json_str):
    d = json.loads(json_str)
    return alarm.Alarm(d["id"], d["citizen"], d["status"])


def parse_citizen(json_str):
    d = json.loads(json_str)
    return citizen.Citizen(d["id"], d["name"], d["email"], d["username"], d["contacts"], d["devices"], d["settings"])


def parse_citizen_admin(json_str):
    d = json.loads(json_str)
    return citizen_admin.CitizenAdmin(d["id"], d["name"], d["email"], d["username"], d["citizens"])


def parse_contact(json_str):
    d = json.loads(json_str)
    return contact.Contact(d["id"], d["name"], d["email"], d["username"], d["phone"], d["devices"])


def parse_device(json_str):
    d = json.loads(json_str)
    return device.Device(d["type"])


def parse_settings(json_str):
    d = json.loads(json_str)
    return settings.Settings


def parse_user(json_str):
    d = json.loads(json_str)
    return user.User(d["id"], d["name"], d["email"], d["username"])


def parse_user_admin(json_str):
    d = json.loads(json_str)
    return user_admin.UserAdmin(d["id"], d["name"], d["email"], d["username"])
