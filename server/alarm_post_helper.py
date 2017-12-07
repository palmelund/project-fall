from model import alarm
from model.user import Citizen

# Note: This file should not be called directly.
# Please use alarm_activate instead.


def lambda_handler(event, context):
    try:
        ctz = Citizen.get(event["id"]) # deserialize(event["citizen"])
    except Exception as ex:
        return None

    if not ctz:
        return None

    this_alarm = alarm.Alarm(-1, ctz, None)

    this_alarm.set()

    return this_alarm.serialize()
