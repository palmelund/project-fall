from enum import Enum


class DeviceType(Enum):
    App = "App"
    PersonalAssistance = "PersonalAssistance"


class Device:
    'A specialized user, representing a contact'

    def __init__(self, id, type):
        self.type = type
        self.id = id
