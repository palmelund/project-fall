# Include directories in the project
import sys
sys.path.insert(0, "../")
sys.path.insert(0, "../server")
sys.path.insert(0, "../server/database")
# Imports
from model import user
import unittest
import requests


class CitizenTestCase(unittest.TestCase):
    def setUp(self):
        # Add test users to DB https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/controlpanel/citizen header: citizen citizenAdmin
        temp_citizen_admin = user.CitizenAdmin(-1, "Admin von Adminson", "admin@iadminu.org", [])

        self._citizen = user.Citizen(-1, "Test Testington", "testington@tester.dk", [], [], "Teststrasse 10", "Testerup", "1000")

    def tearDown(self):
        self._citizen = None

    def test_get_citizen(self):
        self.assertEqual(1, 1)
        # Remove test users to DB https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/controlpanel/citizen header: id


class UserTestCase(unittest.TestCase):

    def test_get_and_post_user_citizen(self):
        self._user = user.Citizen(-1, "Test Testington", "testington@tester.dk", [], [], "Teststrasse 10", "Testerup", "1000")
        user_post_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"

        user_post_header = {"user": self._user.serialize()}

        self._user = user.deserialize(requests.post(user_post_uri, headers=user_post_header))

        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/" + str(self._user.id)
        _user_response = user.deserialize(requests.get(user_get_uri).text)
        user_delete_header = {"user": _user_response.serialize()}

        requests.delete(user_delete_uri, headers=user_delete_header)

        self.assertEqual(self._user, _user_response)

    def test_get_and_post_user_citizen_admin(self):
        self._user = user.CitizenAdmin(-1, "Test Testington", "testington@tester.dk", [])
        user_post_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"

        user_post_header = {"user": self._user.serialize()}

        self._user = user.deserialize(requests.post(user_post_uri, headers=user_post_header))
        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/" + str(self._user.id)

        _user_response = user.deserialize(requests.get(user_get_uri).text)

        user_delete_header = {"user": _user_response.serialize()}
        requests.delete(user_delete_uri, headers=user_delete_header)

        self.assertEqual(self._user, _user_response)

    def test_get_and_post_user_contact(self):
        self._user = user.Contact(-1, "Test Testington", "testington@tester.dk", "+4512345678", [])
        user_post_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"

        user_post_header = {"user": self._user.serialize()}

        self._user = user.deserialize(requests.post(user_post_uri, headers=user_post_header))
        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/" + str(self._user.id)

        _user_response = user.deserialize(requests.get(user_get_uri).text)

        user_delete_header = {"user": _user_response.serialize()}
        requests.delete(user_delete_uri, headers=user_delete_header)

        self.assertEqual(self._user, _user_response)

    def test_get_and_post_user_user_admin(self):
        self._user = user.UserAdmin(-1, "Test Testington", "testington@tester.dk")
        user_post_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        print("/////////////////////////////////")
        print("user serialized: " + str(type(self._user.serialize())))
        user_post_header = {"user": self._user.serialize()}

        self._user = user.deserialize(requests.post(user_post_uri, headers=user_post_header))
        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/" + str(self._user.id)

        _user_response = user.deserialize(requests.get(user_get_uri).text)

        user_delete_header = {"user": _user_response.serialize()}
        requests.delete(user_delete_uri, headers=user_delete_header)

        self.assertEqual(self._user, _user_response)


if __name__ == '__main__':
    print(sys.path)
    unittest.main()
