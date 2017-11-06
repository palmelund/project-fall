class Alarm(User):
    'A specialized user, representing a contact'

    def __init__(self, citizen, status):
        self.status = status
        self.citizen = citizen
