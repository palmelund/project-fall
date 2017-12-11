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
    print("+++++++++++++++++++++++++++++")
    print(response.text)
    print("+++++++++++++++++++++++++++++")
    return str(json.loads(response.content.decode())["body"])


class CitizenTestCase(unittest.TestCase):
    def setUp(self):
        # Add test users to DB https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/controlpanel/citizen header: citizen citizenAdmin
        # temp_citizen_admin = user.CitizenAdmin(-1, "Admin von Adminson", "admin@iadminu.org", [])
        # citizen_admin_header = {"user": temp_citizen_admin.serialize()}

        # admin_id = user.deserialize(get_response(requests.post("https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/", headers=citizen_admin_header))).id
        self._citizen = user.Citizen(-1, "Test Testington", "testington@tester.dk", [user.Contact(-1, "Contactium", "contactium@tester.dk", [])], [], "Teststrasse 10", "Testerup", "1000")

        citizen_header = {"user": self._citizen.serialize().replace("\"", "\\\"")}

        self._citizen = user.deserialize(get_response(requests.post("https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/", headers=citizen_header)))

    def tearDown(self):
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_header = {"user": self._citizen.serialize().replace("\"", "\\\""), "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoidXNlckFkbWluIn0._zMvLSI7elh4ebv-1iaE8nXYdbzjyvpBNlDNhNSJMc0"}
        print("------------ delete user: " + str(self._citizen.serialize().replace("\"", "\\\"")))
        print("------------ delete response: " + str(requests.delete(user_delete_uri, headers=user_delete_header).text))

    def test_get_citizen(self):
        user_get_header = {'token': self._citizen.token}
        #print("token: " + str(user_get_header))
        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/citizen/" + str(self._citizen.id)

        _citizen_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))

        self._citizen.token = ""
        _citizen_response.token = ""

        self.assertDictEqual(json.loads(self._citizen.serialize().replace("'", "\"")), json.loads(_citizen_response.serialize().replace("'", "\"")))


class ContactTestCase(unittest.TestCase):
    def setUp(self):
        # Add test users to DB https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/controlpanel/citizen header: citizen citizenAdmin
        # temp_citizen_admin = user.CitizenAdmin(-1, "Admin von Adminson", "admin@iadminu.org", [])
        # citizen_admin_header = {"user": temp_citizen_admin.serialize()}

        # admin_id = user.deserialize(get_response(requests.post("https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/", headers=citizen_admin_header))).id
        self._contact = user.Contact(-1, "Contactium", "contactium@tester.dk", [])

        contact_header = {"user": self._contact.serialize().replace("\"", "\\\"")}
        self._contact = user.deserialize(get_response(requests.post("https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/", headers=contact_header)))

    def tearDown(self):
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_header = {"user": self._contact.serialize().replace("\"", "\\\""), "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoidXNlckFkbWluIn0._zMvLSI7elh4ebv-1iaE8nXYdbzjyvpBNlDNhNSJMc0"}
        requests.delete(user_delete_uri, headers=user_delete_header).text

    def test_get_contact(self):
        user_get_header = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoidXNlckFkbWluIn0._zMvLSI7elh4ebv-1iaE8nXYdbzjyvpBNlDNhNSJMc0"}
        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/contact/" + str(self._contact.id)

        _citizen_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))
        self._contact.token = ""
        _citizen_response.token = ""
        self.assertDictEqual(json.loads(self._contact.serialize().replace("'", "\"")), json.loads(_citizen_response.serialize().replace("'", "\"")))


class UserTestCase(unittest.TestCase):

    def test_get_and_post_user_citizen(self):
        _user = user.Citizen(-1, "Test Testington", "citizen@tester.dk", [], [], "Teststrasse 10", "Testerup", "1000")
        user_post_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"

        user_post_header = {"user": _user.serialize().replace("\"", "\\\""), "password": "1234"}
        user_get_header = {"email": "citizen@tester.dk", "password": "1234"}
        print("Post:")
        _user = user.deserialize(get_response(requests.post(user_post_uri, headers=user_post_header)))

        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        print("Get:")
        _user_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))
        user_delete_header = {"user": _user_response.serialize().replace("\"", "\\\""), "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoidXNlckFkbWluIn0._zMvLSI7elh4ebv-1iaE8nXYdbzjyvpBNlDNhNSJMc0"}

        _delete_response = user.deserialize(get_response(requests.delete(user_delete_uri, headers=user_delete_header)))

        _user.token = ""
        _user_response.token = ""

        self.assertDictEqual(json.loads(_user.serialize().replace("'", "\"")), json.loads(_user_response.serialize().replace("'", "\"")))
        self.assertEqual(-1, _delete_response.id)

    def test_get_and_post_user_citizen_admin(self):
        _user = user.CitizenAdmin(-1, "Test Testington", "cadmin@tester.dk", [])
        user_post_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"

        user_post_header = {"user": _user.serialize().replace("\"", "\\\""), "password": "1234"}
        user_get_header = {"email": "cadmin@tester.dk", "password": "1234"}

        _user = user.deserialize(get_response(requests.post(user_post_uri, headers=user_post_header)))

        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        _user_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))
        user_delete_header = {"user": _user_response.serialize().replace("\"", "\\\""), "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoidXNlckFkbWluIn0._zMvLSI7elh4ebv-1iaE8nXYdbzjyvpBNlDNhNSJMc0"}

        _delete_response = user.deserialize(get_response(requests.delete(user_delete_uri, headers=user_delete_header)))

        _user.token = ""
        _user_response.token = ""

        self.assertDictEqual(json.loads(_user.serialize().replace("'", "\"")), json.loads(_user_response.serialize().replace("'", "\"")))
        self.assertEqual(-1, _delete_response.id)

    def test_get_and_post_user_contact(self):
        _user = user.Contact(-1, "Test Testington", "contact@tester.dk", [])
        user_post_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"

        user_post_header = {"user": _user.serialize().replace("\"", "\\\""), "password": "1234"}
        user_get_header = {"email": "contact@tester.dk", "password": "1234"}

        _user = user.deserialize(get_response(requests.post(user_post_uri, headers=user_post_header)))

        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        _user_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))
        user_delete_header = {"user": _user_response.serialize().replace("\"", "\\\""), "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoidXNlckFkbWluIn0._zMvLSI7elh4ebv-1iaE8nXYdbzjyvpBNlDNhNSJMc0"}

        _delete_response = user.deserialize(get_response(requests.delete(user_delete_uri, headers=user_delete_header)))

        _user.token = ""
        _user_response.token = ""

        self.assertDictEqual(json.loads(_user.serialize().replace("'", "\"")), json.loads(_user_response.serialize().replace("'", "\"")))
        self.assertEqual(-1, _delete_response.id)

    def test_get_and_post_user_user_admin(self):
        _user = user.UserAdmin(-1, "Test Testington", "uadmin@tester.dk")
        user_post_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"

        user_post_header = {"user": _user.serialize().replace("\"", "\\\""), "password": "1234"}
        user_get_header = {"email": "uadmin@tester.dk", "password": "1234"}

        _user = user.deserialize(get_response(requests.post(user_post_uri, headers=user_post_header)))

        user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        _user_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))
        user_delete_header = {"user": _user_response.serialize().replace("\"", "\\\""), "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoidXNlckFkbWluIn0._zMvLSI7elh4ebv-1iaE8nXYdbzjyvpBNlDNhNSJMc0"}

        _delete_response = user.deserialize(get_response(requests.delete(user_delete_uri, headers=user_delete_header)))

        _user.token = ""
        _user_response.token = ""

        self.assertDictEqual(json.loads(_user.serialize().replace("'", "\"")), json.loads(_user_response.serialize().replace("'", "\"")))
        self.assertEqual(-1, _delete_response.id)


if __name__ == '__main__':
    unittest.main()
