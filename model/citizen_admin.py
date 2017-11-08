from model.user import *


class CitizenAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, username, citizens):
        super().__init__(id, name, email, username)
        self.citizens = citizens
