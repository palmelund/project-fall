from database import database_manager
from model.user import *
from model import user


class Alarm:

    def __init__(self, status, activatedby, responder):
        self.status = status
        self.activatedby = activatedby
        self.responder = responder

    @staticmethod
    def get(citizenID):
        return database_manager.get_alarm(citizenID)

    def set(self):
        if not self.responder:
            self.status = self.status + 1

        database_manager.set_alarm(self)


def deserialize(mapping):
    return Alarm(mapping["status"], user.deserialize(mapping["activatedby"]), user.deserialize(mapping["responder"]))
