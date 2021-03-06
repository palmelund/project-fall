import psycopg2
from server.database.connect_str import connect_str

try:
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("CREATE TYPE userrole AS ENUM ('contact', 'citizenAdmin', 'citizen', 'userAdmin')")
    # cursor.execute("CREATE TYPE devicetype AS ENUM ('app', 'smartassistance', 'ifttt')")

    # Database setup
    cursor.execute(
        "CREATE TABLE users (id SERIAL PRIMARY KEY, username varchar(50), password varchar(200), salt varchar(50), name varchar(255), email varchar(255), role userrole);")

    cursor.execute("CREATE TABLE contact (userID int REFERENCES users(id) PRIMARY KEY, phone varchar(55));")

    cursor.execute(
        "CREATE TABLE contact (userID int REFERENCES users(id) PRIMARY KEY, phone varchar(55));")
    cursor.execute(
        "CREATE TABLE citizen (userID int REFERENCES users(id) PRIMARY KEY, address varchar(255), city varchar(255), postnr varchar(55), managedBy int REFERENCES users(id));")
    cursor.execute(
        "CREATE TABLE devicemap (token text PRIMARY KEY, deviceid int REFERENCES device(id));")
    cursor.execute(
        "CREATE TABLE device (id SERIAL PRIMARY KEY, content text, devicetype varchar(50));")
    cursor.execute(
        "CREATE TABLE hasa (userID int REFERENCES users(id), deviceID int REFERENCES device(id), PRIMARY KEY(userID, deviceID));")
    cursor.execute(
        "CREATE TABLE associateswith (citizenID int REFERENCES citizen(userID), contactID int REFERENCES contact(userID), PRIMARY KEY(citizenID, contactID));")
    cursor.execute(
        "CREATE TABLE alarm (status int, activatedby int PRIMARY KEY REFERENCES citizen(userID), responder int REFERENCES contact(userID));")
    cursor.execute(
        "CREATE TABLE citizenadmin (userid INT PRIMARY KEY REFERENCES users(id));"
    )
    cursor.execute(
        "CREATE TABLE manages (adminid INTEGER REFERENCES citizenadmin(userid), citizenid INTEGER REFERENCES citizen(userid), PRIMARY KEY (adminid, citizenid));"
    )
    cursor.execute(
        "CREATE TABLE useradmin (id SERIAL PRIMARY KEY);"
    )

    conn.commit()
    cursor.close()
    conn.close()

except Exception as e:
    print(e)
