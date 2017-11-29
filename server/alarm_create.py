from model import alarm
from model.user import deserialize, User
from respond import build_response_no_ser
from sns import sns_interface
import json
from pprint import pprint
import boto3

def lambda_handler(event, context):
    try:
        citizen = deserialize(json.loads(event["citizen"]))
        citizen = User.get(citizen.id)
    except Exception as ex:
        return build_response_no_ser("400", "Missing arguments 1!")

    if not citizen:
        return build_response_no_ser("400", "Missing arguments 2!")

    this_alarm = alarm.Alarm(0, citizen, None)

    this_alarm.set()

    # Notify contacts
    sns_interface.push_all(citizen.contacts, "message")

    # sms contacts
    sns_interface.send_all(citizen.contacts, "message")

    # Get phone numbers:
    numbers = set([])

    for c in citizen.contacts:
        for d in c.devices:
            content = json.loads(d.content)
            if content["messagetype"] == "call":
                numbers.add(c.phone)

    return build_response_no_ser("200", {
        "responstype": "createalarm",
        "numberlist": json.dumps(list(numbers))
    })
