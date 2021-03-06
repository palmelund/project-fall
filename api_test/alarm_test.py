# Include directories in the project
import sys
sys.path.insert(0, "../")
sys.path.insert(0, "../server")
sys.path.insert(0, "../server/database")
# Imports
from model.alarm import Alarm
from model import alarm
from model import user
import unittest
import requests
import json
from pprint import pprint

def get_response(response):
    print("+++++++++++++++++++++++++++++")
    print(response.text)
    print("+++++++++++++++++++++++++++++")
    return str(json.loads(response.content.decode())["body"])


class AlarmTestCase(unittest.TestCase):
    def test_alarm_post_get_delete(self):
        self._alarm = Alarm(0, self._citizen, None)
        alarm_post_header = {"alarm": self._alarm.serialize().replace("\"", "\\\""), "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoiY2l0aXplbiJ9.Lk0L4BX6Dx0b6PlfWMlSp3xFv5o7lYmya2PyAc-FQdE"}

        alarm_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/citizen/" + str(self._citizen.id) + "/alarm"
        print("Post")
        self._alarm = alarm.deserialize(get_response(requests.post(alarm_uri, headers=alarm_post_header)))
        self._alarm_response = alarm.deserialize(get_response(requests.get(alarm_uri,  headers=alarm_post_header)))

        alarm_delete_header = {"alarm": self._alarm.serialize().replace("\"", "\\\""), "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoidXNlckFkbWluIn0._zMvLSI7elh4ebv-1iaE8nXYdbzjyvpBNlDNhNSJMc0"}
        alarm_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/citizen/" + str(self._citizen.id) + "/alarm"

        _alarm_delete = alarm.deserialize(get_response(requests.delete(alarm_uri, headers=alarm_delete_header)))
        pprint(_alarm_delete.__dict__)
        self.assertDictEqual(json.loads(self._alarm.serialize().replace("'", "\"").replace("None", "null")), json.loads(self._alarm_response.serialize().replace("'", "\"").replace("None", "null")))
        self.assertEqual(-1, _alarm_delete.status)



    def setUp(self):
        self._citizen = user.Citizen(-1, "Test Testington", "testington@tester.dk", [], [], "Teststrasse 10", "Testerup", "1000")

        citizen_header = {"user": self._citizen.serialize().replace("\"", "\\\"")}
        self._citizen = user.deserialize(get_response(requests.post("https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/", headers=citizen_header)))

    def tearDown(self):
        user_delete_uri = "https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user/"
        user_delete_header = {"user": self._citizen.serialize().replace("\"", "\\\""), "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMjM0IiwidXNlcl9yb2xlIjoidXNlckFkbWluIn0._zMvLSI7elh4ebv-1iaE8nXYdbzjyvpBNlDNhNSJMc0"}
        print("------------ delete user: " + str(self._citizen.serialize()))
        print("------------ delete response: " + str(requests.delete(user_delete_uri, headers=user_delete_header).text))


if __name__ == '__main__':
    unittest.main()
