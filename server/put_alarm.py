from connect_str import connect_str
from respond import respond, build_response_no_par


def lambda_handler(event, context):

    try:
        alarm = parse_alarm(event["alarm"])
    except Exception as ex:
        return build_response_no_par("400", "Missing arguments!")

    if not alarm:
        return build_response_no_par("400", "Missing arguments!")

    alarm.set()

    return respond(None)
