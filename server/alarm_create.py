from model import alarm
from model.alarm import Alarm
from model.user import deserialize, User
import json
from json_serializer import JsonSerializer
from respond import build_response_no_ser

# Note: This file should not be called directly.
# Please use alarm_activate instead.


def lambda_handler(event, context):
    try:
        citizen = deserialize(json.loads(event["citizen"]))
        citizen = User.get(citizen.id)
    except Exception as ex:
        return build_response_no_ser("400", {"status": "error"})

    if not citizen:
        return build_response_no_ser("400", {"status": "error"})

    this_alarm: Alarm = alarm.Alarm(0, citizen, None)

    this_alarm.set()

    res = json.dumps(this_alarm.working_serializer(), cls=JsonSerializer)
    return res  # TODO: Proper message format