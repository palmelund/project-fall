from marshmallow import Schema, fields, post_load
from model import user
from model import device
from model import alarm


class DeviceSchema(Schema):
    id = fields.Int()
    devicetype = fields.Str()
    messagetype = fields.Str()
    content = fields.Str(missing=None)

    @post_load
    def make_device(self, data):
        return device.Device(**data)


class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    role = fields.Str()

    @post_load
    def make_user(self, data):
        return user.User(**data)


class ContactSchema(UserSchema):
    devices = fields.Nested(DeviceSchema, many=True, missing=[])

    @post_load
    def make_contact(self, data):
        return user.Contact(**data)


class CitizenSchema(UserSchema):
    contacts = fields.Nested(ContactSchema, many=True, missing=[])
    devices = fields.Nested(DeviceSchema, many=True, missing=[])
    address = fields.Str()
    city = fields.Str()
    postnr = fields.Str()

    @post_load
    def make_citizen(self, data):
        return user.Citizen(**data)


class CitizenAdminSchema(UserSchema):
    citizens = fields.Nested(CitizenSchema, many=True, missing=[])

    @post_load
    def make_citizen_admin(self, data):
        return user.CitizenAdmin(**data)


class UserAdminSchema(UserSchema):
    @post_load
    def make_user_admin(self, data):
        return user.UserAdmin(**data)


class AlarmSchema(Schema):
    status = fields.Int()
    activatedby = fields.Nested(CitizenSchema)
    responder = fields.Nested(ContactSchema, missing=None)

    @post_load
    def make_alarm(self, data):
        return alarm.Alarm(**data)
