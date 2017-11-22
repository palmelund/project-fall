import psycopg2
from connect_str import connect_str
import hashlib
import uuid

# Hashing currently implemented using the code found on stackoverflow
# https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python


def add_user(username, email, password, name, role):
    print("add_user")
    # TODO: Avoid duplicate database entries
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    salt = get_salt()
    hashed_password = hash_password(password, salt)

    print("Salt: " + salt)
    print("Hashed Password: " + hashed_password)

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        exist = cursor.fetchone()

        if exist:
            return None

        cursor.execute("INSERT INTO users VALUES (DEFAULT, %s, %s, %s, %s, %s, %s);", (username, hashed_password, salt, name, email, role))
        print("check")
        cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        print("check")
        user = cursor.fetchone()
        print("User:")
        print(user)
    except Exception as err:
        print(err)
        return None

    conn.commit()
    cursor.close()
    conn.close()

    if not user:
        print("Not user")
        return None

    return user


def login(email, password):
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", [email])
    user = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not user:
        return None

    if check_password(password, user[2], user[3]):
        return user
    else:
        return None


def get_salt():
    return uuid.uuid4().hex


def hash_password(password, salt):
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


def check_password(password, hashed_password, salt):
    return hashed_password == hash_password(password, salt)
