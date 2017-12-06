from server.database import database_manager
from model import schemas


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
        else:
            raise Exception("Invalid role")

    def serialize(self):
        return str(schemas.UserSchema().dump(self).data)


class CitizenAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, citizens):
        super().__init__(id, name, email, "citizenadmin")
        self.citizens = citizens

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

    def serialize(self):
        return str(schemas.CitizenSchema().dump(self).data)


class Contact(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email, devices):
        super().__init__(id, name, email, "contact")
        self.devices = devices

    def serialize(self):
        return str(schemas.ContactSchema().dump(self).data)


class UserAdmin(User):
    'A specialized user, representing a contact'

    def __init__(self, id, name, email):
        super().__init__(id, name, email, "useradmin")

    def serialize(self):
        return str(schemas.UserAdminSchema().dump(self).data)


def deserialize(jsonstring):
    usr: User = schemas.UserSchema().load(jsonstring).data
    if usr.role == "citizen":
        return schemas.CitizenSchema().load(jsonstring).data
    elif usr.role == "contact":
        return schemas.ContactSchema().load(jsonstring).data
    elif usr.role == "citizenAdmin":
        return schemas.CitizenAdminSchema().load(jsonstring).data
    elif usr.role == "userAdmin":
        return schemas.UserAdminSchema().load(jsonstring).data
    else:
        raise Exception("Invalid role!")
