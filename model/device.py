from enum import Enum
from database import database_manager


class DeviceType(Enum):
    App = "App"
    PersonalAssistance = "PersonalAssistance"
    IFTTT = "IFTTT"


class Device:

    def __init__(self, id, type, content):
        self.type = DeviceType(type)
        self.id = id
        self.content = content

    @staticmethod
    def get(deviceID):
        return database_manager.get_device(deviceID)

    def put(self, user):
        database_manager.set_device(self, user)


def deserialize(mapping):
    return Device(mapping["id"], mapping["type"], mapping["content"])
