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
    x = json.loads(jsonstring.replace("'", "\"").replace("None", "null"))
    dvc = schemas.DeviceSchema().load(x).data

    if dvc.devicetype == "appdevice":
        return schemas.AppDeviceSchema().load(x).data
    elif dvc.devicetype == "alexadevice":
        return schemas.AlexaDeviceSchema().load(x).data
    elif dvc.devicetype == "iftttdevice":
        return schemas.IFTTTDeviceSchema().load(x).data
    elif dvc.devicetype == "smsdevice":
        return schemas.SmsDeviceSchema().load(x).data
    elif dvc.devicetype == "phonecalldevice":
        return schemas.PhoneCallDeviceSchema().load(x).data
    else:
        raise Exception
