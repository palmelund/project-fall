from model.user import *


class Contact(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, username, phone, devices):
        super().__init__(id, name, email, username)
        self.phone = phone
        self.devices = devices
