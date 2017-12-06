from server.respond import respond
from model import alarm


def lambda_handler(event, context):
    try:
        id = event["id"]
    except:
        return respond("400", alarm.Alarm(-1, None, None))

    if not id:
        return respond("400", alarm.Alarm(-1, None, None))

    alm = alarm.Alarm.get(id())

    if not alm or alm.activatedby == -1:
        return respond("400", alarm.Alarm(-1, None, None))
    else:
        return respond("200", alm.serialize())
