from model.user import *


class UserAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, name, email, username):
        super().__init__(name, email, username)
