from server.database import database_manager
from model import schemas
import json
import string

alexa = "alexa"
smartphone = "smartphone"
ifttt = "ifttt"


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

    def put(self, user):
        database_manager.set_device(self, user)

    def update(self):
        database_manager.update_device(self)

    def delete(self):
        database_manager.delete_device(self.id)

    def get_owner(self):
        return database_manager.get_device_owner(self.id)

    def serialize(self):
        return str(schemas.DeviceSchema().dump(self).data)


class AppDevice(Device):
    def __init__(self, device_id, token, arn):
        super.__init__(device_id, "appdevice")
        self.token = token
        self.arn = arn

    def notify(self, activatedby):



class AlexaDevice(Device):

    def __init__(self, device_id, user_id):
        super.__init__(device_id, "alexadevice")
        self.user_id = user_id


class IFTTTDevice(Device):

    def __init__(self, device_id, token):
        super.__init__(device_id, "iftttdevice")
        self.token = token


class SmsDevice(Device):
    def __init__(self, device_id, phone_number):
        super.__init__(device_id, "smsdevice")
        self.phone_number = phone_number


class PhoneCallDevice(Device):
    def __init__(self, device_id, phone_number):
        super.__init__(device_id, "phonecalldevice")
        self.phone_number = phone_number


def deserialize(jsonstring):
    return schemas.DeviceSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
