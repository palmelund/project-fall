from marshmallow import Schema, fields, post_load
from model import user
from model import device
from model import alarm
from pprint import pprint


class DeviceSchema(Schema):
    id = fields.Int()
    devicetype = fields.Str()

    @post_load
    def make_device(self, data):
        return device.Device(data["id"], data["devicetype"])


class AppDeviceSchema(Schema):
    id = fields.Int()
    devicetype = fields.Str()
    token = fields.Str()
    arn = fields.Str()

    @post_load
    def make_app_device(self, data):
        return device.AppDevice(data["id"], data["token"], data["arn"])


class AlexaDeviceSchema(Schema):
    id = fields.Int()
    devicetype = fields.Str()
    user_id = fields.Str()

    @post_load
    def make_alexa_device(self, data):
        return device.AlexaDevice(data["id"], data["user_id"])


class IFTTTDeviceSchema(Schema):
    id = fields.Int()
    devicetype = fields.Str()
    token = fields.Str()

    @post_load
    def make_ifttt_device(self, data):
        return device.IFTTTDevice(data["id"], data["token"])


class SmsDeviceSchema(Schema):
    id = fields.Int()
    devicetype = fields.Str()
    phone_number = fields.Str()

    @post_load
    def make_sms_device(self, data):
        return device.SmsDevice(data["id"], data["phone_number"])


class PhoneCallDeviceSchema(Schema):
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
        return user.Contact(data["id"], data["name"], data["email"], data["devices"])


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
        return user.Citizen(data["id"], data["name"], data["email"], data["contacts"], data["devices"], data["address"], data["city"], data["postnr"])


class CitizenAdminSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    role = fields.Str()
    citizens = fields.Nested(CitizenSchema, many=True, missing=[])
    token = fields.Str(missing="")

    @post_load
    def make_citizen_admin(self, data):
        return user.CitizenAdmin(data["id"], data["name"], data["email"], data["citizens"])


class UserAdminSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    role = fields.Str()
    token = fields.Str(missing="")

    @post_load
    def make_user_admin(self, data):
        return user.UserAdmin(data["id"], data["name"], data["email"])


class AlarmSchema(Schema):
    status = fields.Int()
    activatedby = fields.Nested(CitizenSchema, missing=None)
    responder = fields.Nested(ContactSchema, missing=None)

    @post_load
    def make_alarm(self, data):
        return alarm.Alarm(data["status"], data["activatedby"], data["responder"])
