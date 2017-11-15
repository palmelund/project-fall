from connect_str import connect_str
from respond import respond
import psycopg2


def lambda_handler(event, context):
    # Create an alarm
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO alarm VALUES (DEFAULT, %s, %s, NULL )", (0, event['userid']))

    # TODO: Create logic to get help

    # TODO: Remove finished alarm

    conn.commit()
    cursor.close()
    conn.close()

    return respond(None, "Created Alarm")
