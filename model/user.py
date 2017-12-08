from server.database import database_manager
from model import schemas
import json
from typing import List


class User:
    'Generalization of different user types'

    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

    @staticmethod
    def attempt_login(email, password):
        return database_manager.login(email, password)

    @staticmethod
    def get(user_id):
        return database_manager.get_user(user_id)

    def update(self):
        database_manager.update_user(self)

    def delete(self):
        database_manager.delete_user(self.id)

    @staticmethod
    def create_new_user(name, email, password, role, address=None, city=None, zipcode=None, managed_by=None, phone=None):
        usr = database_manager.add_user(email, password, name, role)

        if not usr:
            raise Exception("Could not create user")

        if role == "citizen":
            return database_manager.add_citizen(usr.id, address, city, zipcode, managed_by)
        elif role == "contact":
            return database_manager.add_contact(usr.id)
        elif role == "citizenAdmin":
            return database_manager.add_citizen_admin(usr.id)
        elif role == "userAdmin":
            return database_manager.add_user_admin(usr.id)
        else:
            raise Exception("Invalid role")

    def serialize(self):
        return str(schemas.UserSchema().dump(self).data)


class CitizenAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, citizens):
        super().__init__(id, name, email, "citizenAdmin")
        self.citizens = citizens

    def update(self):

        old_citizens = database_manager.get_citizen_admins_citizens(self.id)

        added_citizens = List(set(self.citizens)-set(old_citizens))
        removed_citizens = List(set(old_citizens)-set(self.citizens))

        database_manager.update_citizen_admin(self, added_citizens, removed_citizens)
        super().update()

    def delete(self):
        database_manager.delete_citizen_admin(self.id)

    def serialize(self):
        return str(schemas.CitizenAdminSchema().dump(self).data)


class Citizen(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, contacts, devices, address, city, postnr):
        super().__init__(id, name, email, "citizen")
        self.contacts = contacts
        self.devices = devices
        self.address = address
        self.city = city
        self.postnr = postnr

    def update(self):

        old_devices = database_manager.get_user_devices(self.id)
        old_contacts = database_manager.get_user_devices(self.id)

        added_devices = List(set(self.devices)-set(old_devices))
        removed_devices = List(set(old_devices)-set(self.devices))

        added_contacts = List(set(self.contacts)-set(old_contacts))
        removed_contacts = List(set(old_contacts)-set(self.contacts))

        database_manager.update_citizen(self, added_devices, removed_devices, added_contacts, removed_contacts)

        super().update()

    def delete(self):
        database_manager.delete_citizen(self.id)

    def serialize(self):
        return str(schemas.CitizenSchema().dump(self).data)


class Contact(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, devices):
        super().__init__(id, name, email, "contact")
        self.devices = devices

    def update(self):
        old_devices = database_manager.get_user_devices(self.id)

        added_devices = List(set(self.devices)-set(old_devices))
        removed_devices = List(set(old_devices)-set(self.devices))

        database_manager.update_contact(self.id, added_devices, removed_devices)
        super().update()

    def delete(self):
        database_manager.delete_contact(self.id)

    def serialize(self):
        return str(schemas.ContactSchema().dump(self).data)


class UserAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email):
        super().__init__(id, name, email, "userAdmin")

    def update(self):
        # Nothing to update
        x = 0   # Just so it won't complain
        super().update()

    def delete(self):
        database_manager.delete_user_admin(self.id)

    def serialize(self):
        return str(schemas.UserAdminSchema().dump(self).data)


def deserialize(jsonstring):
    usr: User = schemas.UserSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data

    if usr.role == "citizen":
        return schemas.CitizenSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
    elif usr.role == "contact":
        return schemas.ContactSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
    elif usr.role == "citizenAdmin":
        return schemas.CitizenAdminSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
    elif usr.role == "userAdmin":
        return schemas.UserAdminSchema().load(json.loads(jsonstring.replace("'", "\"").replace("None", "null"))).data
    else:
        raise Exception("Invalid role!")
