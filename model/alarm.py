from database import database_manager


class Alarm:

    def __init__(self, status, activatedby, responder):
        self.status = status
        self.citizen = citizen
        self.activatedby = activatedby

    @staticmethod
    def get(alarm_id):
        return database_manager.get_alarm(alarm_id)

    def set():
        if not responder:
            self.status = self.status + 1

        database_manager.set_alarm(self)


def deserialize(mapping):
    return Alarm(mapping["id"], mapping["citizen"], mapping["status"])
