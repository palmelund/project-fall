from database import database_manager
from model.user import *

class Alarm:

    def __init__(self, status, activatedby, responder):
        self.status = status
        self.citizen = citizen
        self.activatedby = activatedby

    @staticmethod
    def get(citizenID):
        return database_manager.get_alarm(citizenID)

    def set():
        if not responder:
            self.status = self.status + 1

        database_manager.set_alarm(self)


def deserialize(mapping):
    return Alarm(mapping["status"], user.deserialize(mapping["activatedby"]), user.deserialize(mapping["responder"]))
