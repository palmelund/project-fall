class User:
    'Generalization of different user types'

    def __init__(self, id, name, email, username):
        self.id = id
        self.name = name
        self.email = email
        self. username = username


class CitizenAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, username, citizens):
        super().__init__(id, name, email, username)
        self.citizens = citizens


class Citizen(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, username, contacts, devices, settings):
        super().__init__(id, name, email, username)
        self.contacts = contacts
        self.devices = devices
        self.settings = settings


class Contact(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, username, phone, devices):
        super().__init__(id, name, email, username)
        self.phone = phone
        self.devices = devices


class UserAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, username):
        super().__init__(id, name, email, username)
