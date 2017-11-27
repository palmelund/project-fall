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

    _alarm = Alarm(0, citizen, None)
    _alarm.put()

    for x in range[0, 30]:
        temp_alarm = alarm.get(citizen.id)

        if temp_alarm.responder:
            return build_response_no_ser("200", citizen.serialize())
