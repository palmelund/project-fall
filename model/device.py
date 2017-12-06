from server.database import database_manager
from model import schemas


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

    def put(self, user):
        database_manager.set_device(self, user)

    def update(self):
        database_manager.update_device(self)

    def get_owner(self):
        return database_manager.get_device_owner(self.id)

    def serialize(self):
        return schemas.DeviceSchema().dump(self).data


def deserialize(jsonstring):
    return schemas.DeviceSchema().load(jsonstring).data
