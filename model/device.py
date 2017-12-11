from server.database import database_manager
from model import schemas
import json
import string


class Device:

    def __init__(self, id, devicetype):
        self.id = id
        self.devicetype = devicetype

    @staticmethod
    def get(deviceID):
        return database_manager.get_device(deviceID)

    @staticmethod
    def get_from_object(user_id):
        return database_manager.get_device_from_user_id(user_id)

    def post(self, user):
        return database_manager.post_device(self, user)

    def put(self):
        database_manager.update_device(self)

    def delete(self):
        database_manager.delete_device(self.id)

    def get_owner(self):
        return database_manager.get_device_owner(self.id)

    def serialize(self):
        return str(schemas.DeviceSchema().dump(self).data)


class AppDevice(Device):
    def __init__(self, device_id, token, arn):
        super().__init__(device_id, "appdevice")
        self.token = token
        self.arn = arn

    def serialize(self):
        return str(schemas.AppDeviceSchema().dump(self).data)


class AlexaDevice(Device):

    def __init__(self, device_id, user_id):
        super().__init__(device_id, "alexadevice")
        self.user_id = user_id

    def serialize(self):
        return str(schemas.AlexaDeviceSchema().dump(self).data)


class IFTTTDevice(Device):

    def __init__(self, device_id, token):
        super().__init__(device_id, "iftttdevice")
        self.token = token

    def serialize(self):
        return str(schemas.IFTTTDeviceSchema().dump(self).data)


class SmsDevice(Device):
    def __init__(self, device_id, phone_number):
        super().__init__(device_id, "smsdevice")
        self.phone_number = phone_number

    def serialize(self):
        return str(schemas.SmsDeviceSchema().dump(self).data)


class PhoneCallDevice(Device):
    def __init__(self, device_id, phone_number):
        super().__init__(device_id, "phonecalldevice")
        self.phone_number = phone_number

    def serialize(self):
        print("O/")
        return str(schemas.PhoneCallDeviceSchema().dump(self).data)


def deserialize(jsonstring):
    _device = schemas.DeviceSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data

    if _device.devicetype == "appdevice":
        return schemas.AppDeviceSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
    elif _device.devicetype == "alexadevice":
        return schemas.AlexaDeviceSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
    elif _device.devicetype == "iftttdevice":
        return schemas.IFTTTDeviceSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
    elif _device.devicetype == "smsdevice":
        return schemas.SmsDeviceSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
    elif _device.devicetype == "phonecalldevice":
        return schemas.PhoneCallDeviceSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
    else:
        return schemas.DeviceSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
