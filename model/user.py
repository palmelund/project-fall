from database import database_manager
import json


def deserialize(load):
    # Citizen
    if len(load) == 8:
        contacts = []
        devices = []

        for contact in load['contacts']:
            contacts.append(deserialize(contact))

        for device in load['devices']:
            contacts.append(**device)

        return Citizen(load['id'], load['name'], load['email'], contacts, devices, load['address'], load['city'], load['postnr'])
    # Contact
    elif len(load) == 5:
        devices = []

        for device in load['devices']:
            contacts.append(**device)

        return Contact(load['id'], load['name'], load['email'], load['phone'], devices)
    # Citizen Admin
    elif len(load) == 4:
        citizens = []

        for citizen in load['citizens']:
            citizens.append(deserialize(citizen))

        return CitizenAdmin(id, load['name'], load['email'], citizens)
    # User Admin
    elif len(load) == 3:
        return UserAdmin(**load)


class User:
    'Generalization of different user types'

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def attempt_login(mail, password):
        return 1

    @staticmethod
    def get(userID):
        return database_manager.get_user(userID)


class CitizenAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, citizens):
        super().__init__(id, name, email)
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

    # @staticmethod
    # def Create(self, id, name, email, contacts, devices, address, city, postnr):


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
