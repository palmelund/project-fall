from enum import Enum


class DeviceType(Enum):
    App = "App"
    PersonalAssistance = "PersonalAssistance"


class Device:

    def __init__(self, type):
        self.type = type
