from model import alarm
from model.alarm import Alarm
from model.user import deserialize
from respond import respond

# Note: This file should not be called directly.
# Please use alarm_activate instead.


def lambda_handler(event, context):
    try:
        citizen = deserialize(event["citizen"])
    except Exception as ex:
        return respond("400", str(ex))

    if not citizen:
        return respond("400", "error")

    this_alarm: Alarm = alarm.Alarm(0, citizen, None)

    this_alarm.set()

    return this_alarm.serialize()
