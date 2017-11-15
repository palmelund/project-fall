from connect_str import connect_str
from respond import respond, build_response
import psycopg2
import time


def lambda_handler(event, context):
    # Create an alarm
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO alarm VALUES (DEFAULT, %s, %s, NULL )", (0, event['userid']))
    conn.commit()

    cursor.execute("SELECT contactid FROM associateswith WHERE citizenid = %s", event['userid'])
    res = cursor.fetchone()

    if res == ():
        return build_response(400, "No contacts found for citizen")
        # TODO: Error, what do we do if there are no contacts?

    status = ()

    for contact in res:
        # TODO: Make contact with contact!
        # TODO: What is an older contact answer after we have moved on?

        for t in range(0, 6):
            time.sleep(1)
            cursor.execute("SELECT * FROM alarm WHERE activatedby = %s", event['userid'])
            status = cursor.fetchone()

            # If someone has reacted on the alarm, stop asking for help.
            if status[1] == -1:
                break
                # If someone has reacted on the alarm, stop asking for help.

        if status[1] == -1:
            break

    if status[1] == -1:
        ""
        # TODO: Let citizen know help is on the way
    else:
        ""
        # TODO: What do we do if noone responds?

    # TODO: Remove finished alarm
    cursor.execute("DELETE FROM alarm WHERE activatedby = %s;", event['userid'])

    conn.commit()
    cursor.close()
    conn.close()

    return respond(None, "Created Alarm")
