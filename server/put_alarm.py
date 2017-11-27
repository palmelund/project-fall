import psycopg2
from connect_str import connect_str
from respond import respond, build_response_no_par
from model.json_parser import parse_alarm, parse_contact


def lambda_handler(event, context):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    try:
        response = event["response"]
        contact = parse_contact(event["contact"])
        alarm = parse_alarm(event["alarm"])
    except Exception as ex:
        return build_response_no_par("400", "Missing arguments!")

    if all(x is not None for x in [response, contact, alarm]):
        return build_response_no_par("400", "Missing arguments!")

    if response == 1:
        cursor.execute("UPDATE alarm SET status = -1, responder = %s WHERE id = %s;", (contact.id, alarm.id))
    else:
        cursor.execute("UPDATE alarm SET status = status + 1 WHERE id = %s;", [alarm.id])

    conn.commit()
    cursor.close()
    conn.close()

    return respond(None)
