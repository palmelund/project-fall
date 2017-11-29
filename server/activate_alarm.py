from connect_str import connect_str
from respond import respond, build_response
from sns import sns_interface
from model.alarm import *
from model.user import *
import time


def lambda_handler(event, context):
    try:
        citizen = user.Citizen.deserialize(event["citizen"])
    except Exception as ex:
        return build_response_no_par("400", "Missing arguments!")

    if not citizen:
        return build_response_no_par("400", "Missing arguments!")

    this_alarm = Alarm(0, citizen, None)
    this_alarm.put()

    # SEND ALARM TO FIRST CONTACT HERE

    timeout = (295 / citizen.contact)
    currenttimer = 0

    for x in citizen.contact:
        temp_alarm = alarm.get(citizen.id)

        if temp_alarm.responder:
            return build_response_no_ser("200", temp_alarm.responder.serialize())
        elif temp_alarm.status < this_alarm.status:
            this_alarm = temp_alarm
            # SEND ALARM TO *status* CONTACT HERE

        if currenttimer > timeout:
            currenttimer = 0
            temp_alarm.status += 1
            temp_alarm.put()

        currenttimer += 5
        time.sleep(5)
