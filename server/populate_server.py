from model.user import User, Contact, Citizen, CitizenAdmin
from model.device import Device
from database.database_manager import associate

def lambda_handler(event, context):

    # Create users

    admin1: CitizenAdmin = User.create_new_user("Citizen Admin 1", "a1", "a1", "citizenAdmin")

    citizen1: Citizen = User.create_new_user("Citizen 1", "c1", "c1", "citizen", address="addr 1", city="city 1", zipcode="zip 1", managed_by=admin1.id)
    citizen2: Citizen = User.create_new_user("Citizen 2", "c2", "c2", "citizen", address="addr 2", city="city 2", zipcode="zip 2", managed_by=admin1.id)
    citizen3: Citizen = User.create_new_user("Citizen 3", "c3", "c3", "citizen", address="addr 3", city="city 3", zipcode="zip 3", managed_by=admin1.id)

    citizena: Citizen = User.create_new_user("a", "a", "b", "citizen", address="addr", city="city", zipcode="zip", managed_by=admin1.id)

    contact1: Contact = User.create_new_user("Contact 1", "k1", "k1", "contact", phone="<phone number>")
    contact2: Contact = User.create_new_user("Contact 2", "k2", "k2", "contact", phone="<phone number>")
    contact3: Contact = User.create_new_user("Contact 3", "k3", "k3", "contact", phone="<phone number>")
    contact4: Contact = User.create_new_user("Contact 4", "k4", "k4", "contact", phone="<phone number>")
    contact5: Contact = User.create_new_user("Contact 5", "k5", "k5", "contact", phone="<phone number>")
    contact6: Contact = User.create_new_user("Contact 6", "k6", "k6", "contact", phone="<phone number>")

    contactb: Contact = User.create_new_user("b", "b", "a", "contact", phone=None)

    # Link citizen and contact

    associate(citizen1.id, contact1.id)
    associate(citizen1.id, contact2.id)
    associate(citizen2.id, contact3.id)
    associate(citizen2.id, contact4.id)
    associate(citizen3.id, contact5.id)
    associate(citizen3.id, contact6.id)

    associate(citizena.id, contactb.id)
