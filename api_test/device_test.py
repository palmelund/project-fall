# Include directories in the project
import sys
sys.path.insert(0, "../")
sys.path.insert(0, "../server")
sys.path.insert(0, "../server/database")
# Imports
from model import device
from model import user
import unittest
import requests
import json


def get_response(response):
        print("+++++++++++++++++++++++++++++")
        print(response.text)
        print("+++++++++++++++++++++++++++++")
        return str(json.loads(response.content.decode())["body"])


class DeviceTestCase(unittest.TestCase):
        def setUp(self):
            self._citizen = user.Citizen(-1, "Test Testington", "testington@tester.dk", [], [], "Teststrasse 10", "Testerup", "1000")

            citizen_header = {"user": self._citizen.serialize().replace("\"", "\\\""), "password": "1234"}

            self._citizen = user.deserialize(get_response(requests.post("https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/", headers=citizen_header)))

        def tearDown(self):
            user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
            user_delete_header = {"user": self._citizen.serialize(), "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoidXNlckFkbWluIn0._zMvLSI7elh4ebv-1iaE8nXYdbzjyvpBNlDNhNSJMc0"}
            # print("------------ delete user: " + str(self._citizen.serialize()))
            # print("------------ delete response: " + str(requests.delete(user_delete_uri, headers=user_delete_header).text))

        def test_device_post(self):
            _device = device.AlexaDevice(-1, "temp_token1234")
            device_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/citizen/" + str(self._citizen.id) + "/device"
            # print(_device.serialize())
            device_header = {"device": _device.serialize(), "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoidXNlckFkbWluIn0._zMvLSI7elh4ebv-1iaE8nXYdbzjyvpBNlDNhNSJMc0"}
            _device = device.deserialize(get_response(requests.post(device_uri, headers=device_header)))

            user_get_header = {"email": "testington@tester.dk", "password": "1234"}
            user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"

            _citizen_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))

            self.assertDictEqual(json.loads(_device.serialize().replace("'", "\"")), json.loads(_citizen_response.devices[0].serialize().replace("'", "\"")))

        def test_device_delete(self):
            _device = device.AlexaDevice(-1, "temp_token1234")
            device_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/citizen/" + str(self._citizen.id) + "/device"
            device_header = {"device": _device.serialize(), "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoidXNlckFkbWluIn0._zMvLSI7elh4ebv-1iaE8nXYdbzjyvpBNlDNhNSJMc0"}
            _device = device.deserialize(get_response(requests.delete(device_uri, headers=device_header)))

            user_get_header = {"email": "testington@tester.dk", "password": "1234"}
            user_get_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/citizen/" + str(self._citizen.id)

            _citizen_response = user.deserialize(get_response(requests.get(user_get_uri, headers=user_get_header)))

            self.assertEqual(len(_citizen_response.devices), 0)


if __name__ == '__main__':
    unittest.main()
