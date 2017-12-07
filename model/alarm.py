from model.schemas import AlarmSchema
from server.database import database_manager
import json
import string

class Alarm:
    def __init__(self, status, activatedby, responder):
        self.status = status
        self.activatedby = activatedby
        self.responder = responder

    @staticmethod
    def get(citizen_id):
        return database_manager.get_alarm(citizen_id)

    def set(self):
        if not self.responder:
            self.status = self.status + 1

        database_manager.set_alarm(self)

    def delete(self):
        database_manager.delete_alarm(self.activatedby.id)

    def serialize(self):
        return str(AlarmSchema().dump(self).data)


def deserialize(jsonstring):
    print("json: " + jsonstring)
    return AlarmSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
