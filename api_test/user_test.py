# Include directories in the project
import sys
sys.path.insert(0, "../")
sys.path.insert(0, "../server")
sys.path.insert(0, "../server/database")
# Imports
from model import user
import unittest
import requests
import json


def get_response(response):
    print("Response:")
    print(response.content.decode())
    print(json.loads(response.content.decode()))
    return json.loads(response.content.decode())["body"]


class CitizenTestCase(unittest.TestCase):
    def setUp(self):
        # Add test users to DB https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/controlpanel/citizen header: citizen citizenAdmin
        temp_citizen_admin = user.CitizenAdmin(-1, "Admin von Adminson", "admin@iadminu.org", [])
        citizen_admin_header = {"user": temp_citizen_admin.serialize()}

        admin_id = user.deserialize(get_response(requests.post("https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/", headers=citizen_admin_header))).id
        self._citizen = user.Citizen(-1, "Test Testington", "testington@tester.dk", [], [], "Teststrasse 10", "Testerup", "1000")

        citizen_header = {"user": self._citizen.serialize()}
        self.citizen_id = user.deserialize(get_response(requests.post("https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/", headers=citizen_header))).id
        self._citizen = user.deserialize(get_response(requests.get("https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/" + self.citizen_id)))

    def tearDown(self):
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_header = {"user": self._citizen.serialize()}
        requests.delete(user_delete_uri, headers=user_delete_header)

    def test_get_citizen(self):
        user_get_header = {"email": "testington@tester.dk", "password": "1234"}
        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        _citizen_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))
        self.assertEqual(self._citizen, _citizen_response)


class UserTestCase(unittest.TestCase):

    def test_get_and_post_user_citizen(self):
        _user = user.Citizen(-1, "Test Testington", "testington@tester.dk", [], [], "Teststrasse 10", "Testerup", "1000")
        user_post_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"

        user_post_header = {"user": _user.serialize(), "password": "1234"}
        user_get_header = {"email": "testington@tester.dk", "password": "1234"}

        _user = user.deserialize(get_response(requests.post(user_post_uri, headers=user_post_header)))

        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        _user_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))
        user_delete_header = {"user": _user_response.serialize()}

        requests.delete(user_delete_uri, headers=user_delete_header)

        self.assertEqual(_user, _user_response)

    def test_get_and_post_user_citizen_admin(self):
        _user = user.CitizenAdmin(-1, "Test Testington", "testington@tester.dk", [])
        user_post_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"

        user_post_header = {"user": _user.serialize(), "password": "1234"}
        user_get_header = {"email": "testington@tester.dk", "password": "1234"}

        _user = user.deserialize(get_response(requests.post(user_post_uri, headers=user_post_header)))

        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        _user_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))
        user_delete_header = {"user": _user_response.serialize()}

        requests.delete(user_delete_uri, headers=user_delete_header)

        self.assertEqual(_user, _user_response)

    def test_get_and_post_user_contact(self):
        _user = user.Contact(-1, "Test Testington", "testington@tester.dk", [])
        user_post_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"

        user_post_header = {"user": _user.serialize(), "password": "1234"}
        user_get_header = {"email": "testington@tester.dk", "password": "1234"}

        _user = user.deserialize(get_response(requests.post(user_post_uri, headers=user_post_header)))

        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        _user_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))
        user_delete_header = {"user": _user_response.serialize()}

        requests.delete(user_delete_uri, headers=user_delete_header)

        self.assertEqual(_user, _user_response)

    def test_get_and_post_user_user_admin(self):
        _user = user.UserAdmin(-1, "Test Testington", "testington@tester.dk")
        user_post_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"

        user_post_header = {"user": _user.serialize(), "password": "1234"}
        user_get_header = {"email": "testington@tester.dk", "password": "1234"}
        print("User: " + str(_user.serialize()))
        _user = user.deserialize(get_response(requests.post(user_post_uri, headers=user_post_header)))

        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        _user_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))
        user_delete_header = {"user": _user_response.serialize()}

        requests.delete(user_delete_uri, headers=user_delete_header)

        self.assertEqual(_user, _user_response)


if __name__ == '__main__':
    print(sys.path)
    unittest.main()
