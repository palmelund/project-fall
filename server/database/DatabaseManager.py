from connect_str import connect_str
from model.user import *
import psycopg2


def get_all_citizens():
    allCitizens = ()

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user, citizen WHERE user.id = citizen.userID")
    citizensRaw = cursor.fetchall()

    for citizen in citizensRaw:
        print(citizen)
