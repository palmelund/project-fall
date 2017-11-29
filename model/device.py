from enum import Enum
from database import database_manager


class DeviceType(Enum):
    App = "App"
    PersonalAssistance = "PersonalAssistance"


class Device:

    def __init__(self, id, type, content):
        self.type = type
        self.id = id
        self.content = content

    @staticmethod
    def get(deviceID):
        return database_manager.get_device(deviceID)


def deserialize(mapping):
    return Device(mapping["id"], mapping["type"], mapping["content"])
