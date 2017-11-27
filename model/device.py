from enum import Enum
from database import database_manager

class DeviceType(Enum):
    App = "App"
    PersonalAssistance = "PersonalAssistance"


class Device:
    'A specialized user, representing a contact'

    def __init__(self, id, type):
        self.type = type
        self.id = id

    @staticmethod
    def get(deviceID):
        return database_manager.get_device(deviceID)
