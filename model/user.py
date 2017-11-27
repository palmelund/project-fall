from database import database_manager


class User:
    'Generalization of different user types'

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

        @staticmethod
        def attempt_login(mail, password):
            return 1

        @staticmethod
        def get(userID):
            return database_manager.get_user(userID)


class CitizenAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, username, citizens):
        super().__init__(id, name, email, username)
        self.citizens = citizens


class Citizen(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, contacts, devices, address, city, postnr):
        super().__init__(id, name, email)
        self.contacts = contacts
        self.devices = devices
        self.address = address
        self.city = city
        self. postnr = postnr


class Contact(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, phone, devices):
        super().__init__(id, name, email)
        self.phone = phone
        self.devices = devices


class UserAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email):
        super().__init__(id, name, email)
