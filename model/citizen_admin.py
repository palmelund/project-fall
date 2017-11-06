from model.user import *


class CitizenAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, name, email, username, citizens):
        super().__init__(name, email, username)
        self.citizens = citizens
