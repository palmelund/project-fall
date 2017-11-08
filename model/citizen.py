from model.user import *


class Citizen(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, username, contacts, devices, settings):
        super().__init__(id, name, email, username)
        self.contacts = contacts
        self.devices = devices
        self.settings = settings
