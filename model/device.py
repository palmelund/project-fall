from enum import Enum
from database import database_manager
import json


class DeviceType(Enum):
    App = "App"
    PersonalAssistance = "PersonalAssistance"


class Device:

    def __init__(self, id, type, content):
        self.type = type
        self.id = id
        self.content = content

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def get(deviceID):
        return database_manager.get_device(deviceID)


def deserialize(mapping):
    return Device(mapping["id"], mapping["type"], mapping["content"])
