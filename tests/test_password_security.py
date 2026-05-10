import sqlite3
from werkzeug.security import check_password_hash

# -----------------------------
# VULNERABLE VERSION CHECK
# -----------------------------
def get_vulnerable_password():

    conn = sqlite3.connect('../vulnerable_app/database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username='admin'")
    result = cursor.fetchone()

    conn.close()

    return result[0]


def test_password_storage_vulnerable():

    password = get_vulnerable_password()

    # SHOULD BE PLAIN TEXT in vulnerable version
    assert password == "admin123"


# -----------------------------
# FIXED VERSION CHECK
# -----------------------------
def get_secure_password():

    conn = sqlite3.connect('../fixed_app/secure.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username='admin'")
    result = cursor.fetchone()

    conn.close()

    return result[0]


def test_password_storage_fixed():

    password = get_secure_password()

    # SHOULD NOT be plain text anymore
    assert password != "admin123"

    # SHOULD look like hashed password
    assert password.startswith("pbkdf2") or password.startswith("scrypt")
