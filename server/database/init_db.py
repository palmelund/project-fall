import psycopg2
from connect_str import connect_str

try:
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("CREATE TYPE userrole AS ENUM ('contact', 'citizenAdmin', 'citizen')")
    cursor.execute("CREATE TYPE devicetype AS ENUM ('app', 'smartAssistance')")

    # Database setup
    cursor.execute(
        "CREATE TABLE users (id SERIAL PRIMARY KEY, username varchar(50), password varchar(200), salt varchar(50), name varchar(255), email varchar(255), role userrole);")

    cursor.execute("CREATE TABLE contact (userID int REFERENCES users(id) PRIMARY KEY, phone varchar(55));")

    cursor.execute(
        "CREATE TABLE contact (userID int REFERENCES users(id) PRIMARY KEY, phone varchar(55));")
    cursor.execute(
        "CREATE TABLE citizen (userID int REFERENCES users(id) PRIMARY KEY, address varchar(255), city varchar(255), postnr varchar(55), managedBy int REFERENCES users(id));")

    # Device
    cursor.execute("CREATE TABLE device (id SERIAL PRIMARY KEY, type devicetype);")

    cursor.execute(
        "CREATE TABLE device (id SERIAL PRIMARY KEY, type devicetype);")
    cursor.execute(
        "CREATE TABLE hasa (userID int REFERENCES users(id), deviceID int REFERENCES device(id), PRIMARY KEY(userID, deviceID));")
    cursor.execute(
        "CREATE TABLE associateswith (citizenID int REFERENCES citizen(userID), contactID int REFERENCES contact(userID), PRIMARY KEY(citizenID, contactID));")
    cursor.execute(
        "CREATE TABLE alarm (id SERIAL PRIMARY KEY, status int, activatedBy int REFERENCES citizen(userID))")
    cursor.execute(
        "CREATE TABLE citizenadmin (userid INT PRIMARY KEY REFERENCES users(id));"
    )
    cursor.execute(
        "CREATE TABLE manages (adminid INTEGER REFERENCES citizenadmin(userid), citizenid INTEGER REFERENCES citizen(userid), PRIMARY KEY (adminid, citizenid));"
    )

    conn.commit()
    cursor.close()
    conn.close()

except Exception as e:
    print(e)
