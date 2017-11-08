from model.user import *


class UserAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, username):
        super().__init__(id, name, email, username)
