from marshmallow import Schema, fields, post_load, post_dump
from model import user
from model import device
from model import alarm
from server.database import database_manager
from pprint import pprint


class DeviceSchema(Schema):
    id = fields.Int()
    devicetype = fields.Str()

    @post_load
    def make_device(self, data):
        return device.Device(data["id"], data["devicetype"])

    @post_dump
    def dismantle_device(self, data):
        print("id: " + str(data))
        dvc = database_manager.get_device(data["id"])
        print(type(dvc))
        return dvc.serialize()


class AppDeviceSchema(DeviceSchema):
    id = fields.Int()
    devicetype = fields.Str()
    token = fields.Str()
    arn = fields.Str()

    @post_load
    def make_app_device(self, data):
        return device.AppDevice(data["id"], data["token"], data["arn"])


class AlexaDeviceSchema(DeviceSchema):
    id = fields.Int()
    devicetype = fields.Str()
    user_id = fields.Str()

    @post_load
    def make_alexa_device(self, data):
        return device.AlexaDevice(data["id"], data["user_id"])


class IFTTTDeviceSchema(DeviceSchema):
    id = fields.Int()
    devicetype = fields.Str()
    token = fields.Str()

    @post_load
    def make_ifttt_device(self, data):
        return device.IFTTTDevice(data["id"], data["token"])


class SmsDeviceSchema(DeviceSchema):
    id = fields.Int()
    devicetype = fields.Str()
    phone_number = fields.Str()

    @post_load
    def make_sms_device(self, data):
        return device.SmsDevice(data["id"], data["phone_number"])


class PhoneCallDeviceSchema(DeviceSchema):
    id = fields.Int()
    devicetype = fields.Str()
    phone_number = fields.Str()

    @post_load
    def make_phone_call_device(self, data):
        return device.PhoneCallDevice(data["id"], data["phone_number"])


class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    role = fields.Str()
    token = fields.Str(missing="")

    @post_load
    def make_user(self, data):
        _user = user.User(data["id"], data["name"], data["email"], data["role"])
        _user.token = data["token"]
        return _user


class ContactSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    role = fields.Str()
    devices = fields.Nested(DeviceSchema, many=True, missing=[])
    token = fields.Str(missing="")

    @post_load
    def make_contact(self, data):
        _user = user.Contact(data["id"], data["name"], data["email"], data["devices"])
        _user.token = data["token"]
        return _user

class CitizenSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    role = fields.Str()
    contacts = fields.Nested(ContactSchema, many=True, missing=[])
    devices = fields.Nested(DeviceSchema, many=True, missing=[])
    address = fields.Str()
    city = fields.Str()
    postnr = fields.Str()
    token = fields.Str(missing="")

    @post_load
    def make_citizen(self, data):
        _user = user.Citizen(data["id"], data["name"], data["email"], data["contacts"], data["devices"], data["address"], data["city"], data["postnr"])
        _user.token = data["token"]
        return _user

class CitizenAdminSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    role = fields.Str()
    citizens = fields.Nested(CitizenSchema, many=True, missing=[])
    token = fields.Str(missing="")

    @post_load
    def make_citizen_admin(self, data):
        _user = user.CitizenAdmin(data["id"], data["name"], data["email"], data["citizens"])
        _user.token = data["token"]
        return _user

class UserAdminSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    role = fields.Str()
    token = fields.Str(missing="")

    @post_load
    def make_user_admin(self, data):
        _user = user.UserAdmin(data["id"], data["name"], data["email"])
        _user.token = data["token"]
        return _user

class AlarmSchema(Schema):
    status = fields.Int()
    activatedby = fields.Nested(CitizenSchema, missing=None)
    responder = fields.Nested(ContactSchema, missing=None)

    @post_load
    def make_alarm(self, data):
        return alarm.Alarm(data["status"], data["activatedby"], data["responder"])
