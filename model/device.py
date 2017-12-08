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
    def get_from_object(obj):
        return database_manager.get_device_from_id(obj["userid"])

    def post(self, user):
        database_manager.post_device(self, user)

    def put(self):
        database_manager.update_device(self)

    def delete(self):
        database_manager.delete_device(self.id)

    def get_owner(self):
        return database_manager.get_device_owner(self.id)

    def serialize(self):

        if self.devicetype == "appdevice":
            return str(schemas.AppDeviceSchema().dump(self).data)
        elif self.devicetype == "alexadevice":
            return str(schemas.AlexaDeviceSchema().dump(self).data)
        elif self.devicetype == "iftttdevice":
            return str(schemas.IFTTTDeviceSchema().dump(self).data)
        elif self.devicetype == "smsdevice":
            return str(schemas.SmsDeviceSchema().dump(self).data)
        elif self.devicetype == "phonecalldevice":
            str(schemas.PhoneCallDeviceSchema().dump(self).data)
        else:
            return str(schemas.DeviceSchema().dump(self).data)


class AppDevice(Device):
    def __init__(self, device_id, token, arn):
        super().__init__(device_id, "appdevice")
        self.token = token
        self.arn = arn


class AlexaDevice(Device):

    def __init__(self, device_id, user_id):
        super().__init__(device_id, "alexadevice")
        self.user_id = user_id


class IFTTTDevice(Device):

    def __init__(self, device_id, token):
        super().__init__(device_id, "iftttdevice")
        self.token = token


class SmsDevice(Device):
    def __init__(self, device_id, phone_number):
        super().__init__(device_id, "smsdevice")
        self.phone_number = phone_number


class PhoneCallDevice(Device):
    def __init__(self, device_id, phone_number):
        super().__init__(device_id, "phonecalldevice")
        self.phone_number = phone_number


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
        raise Exception