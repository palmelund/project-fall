from connect_str import connect_str
from respond import respond, build_response, build_response_no_ser
from model.alarm import Alarm
from model.user import deserialize
from sns import sns_interface
import json
import time


def lambda_handler(event, context):
    try:
        citizen = deserialize(json.loads(event["citizen"]))
    except Exception as ex:
        return build_response_no_ser("400", "Missing arguments 1!")

    if not citizen:
        return build_response_no_ser("400", "Missing arguments 2!")

    this_alarm = Alarm(0, citizen, None)

    this_alarm.set()

    # Send alarm contacts

    timeout = 10  # (295 / citizen.contact)

    for x in citizen.contacts:
        currenttimer = 0
        temp_alarm = Alarm.get(citizen.id)

        if temp_alarm.responder:
            return build_response_no_ser("200", temp_alarm.responder.serialize())
        elif temp_alarm.status < this_alarm.status:
            this_alarm = temp_alarm

            notifycontact(x, this_alarm)

        while True:

            if currenttimer > timeout:
                currenttimer = 0
                temp_alarm.status += 1
                temp_alarm.set()
                break

            currenttimer += 5
            time.sleep(5)


def notifycontact (cnt, alm):
    for d in cnt.devices:
        content = json.loads(d.content)

        if content["type"] == "android":
            if not content["arn"]:
                build_response_no_ser("400", "Missing ARN")

            sns_interface.push_message(content["arn"], json.dumps(alm))

        else:
            return build_response_no_ser("400", "Unsupported device")
