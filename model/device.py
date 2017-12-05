from enum import Enum
from database import database_manager
import json

# We do this in device content instead, and as strings, to make our code simpler.
# Serialization with enums is not worth the troubles

#class DeviceType(Enum):
#    App = "app"
#    PersonalAssistance = "personalassistance"
#    IFTTT = "ifttt"

    #def working_serializer(self):
    #    return self.__dict__

class Device:

    def __init__(self, id, content):
        self.id = id
        self.content = content

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def get(deviceID):
        return database_manager.get_device(deviceID)

    @staticmethod
    def get_from_object(obj):
        return database_manager.get_device_from_id(obj["userid"])

    def put(self, user):
        database_manager.set_device(self, user)

    def update(self, user):
        database_manager.update_device(self, user)

    def get_owner(self):
        return database_manager.get_device_owner(self.id)


    def working_serializer(self):
        return self.__dict__


def deserialize(mapping):
    return Device(mapping["id"], mapping["content"])
