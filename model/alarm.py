from database import database_manager


class Alarm:

    def __init__(self, status, citizen, responder):
        self.status = status
        self.citizen = citizen
        self.responder = responder

    @staticmethod
    def get(alarm_id):
        return database_manager.get_alarm(alarm_id)
