from server.database import database_manager
from model import schemas
import json
import string

alexa = "alexa"
smartphone = "smartphone"
ifttt = "ifttt"


class Device:

    def __init__(self, id, devicetype, messagetype, content):
        self.id = id
        self.content = content
        self.devicetype = devicetype
        self.messagetype = messagetype

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


def deserialize(jsonstring):
    return schemas.DeviceSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
