from model import alarm
from model.alarm import Alarm
from model.user import deserialize

# Note: This file should not be called directly.
# Please use alarm_activate instead.


def lambda_handler(event, context):
    try:
        ctz = deserialize(event["citizen"])
    except Exception as ex:
        return None

    if not ctz:
        return None

    this_alarm: Alarm = alarm.Alarm(0, ctz, None)

    this_alarm.set()

    return this_alarm.serialize()
