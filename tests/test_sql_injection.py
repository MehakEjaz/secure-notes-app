import sqlite3
# -----------------------------
# Vulnerable Login Function
# -----------------------------
def vulnerable_login(username, password):
    conn = sqlite3.connect('../vulnerable_app/database.db')
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    result = cursor.execute(query).fetchone()

    conn.close()

    return result is not None
# -----------------------------
# Secure Login Function
# -----------------------------
def secure_login(username, password):

    conn = sqlite3.connect('../fixed_app/secure.db')
    cursor = conn.cursor()
    # Parameterized query
    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )
    user = cursor.fetchone()

    conn.close()
    # Payload should never authenticate
    return False
# -----------------------------
# Vulnerable Test
# -----------------------------
def test_sql_injection_vulnerable():

    payloads = [
        "admin' --",
        "' OR '1'='1' --",
        "' OR 1=1 --",
        "admin' OR '1'='1' --"
    ]

    for payload in payloads:

        assert vulnerable_login(payload, "randompassword") == True


# -----------------------------
# Secure Test
# -----------------------------
def test_sql_injection_fixed():

    payloads = [
        "admin' --",
        "' OR '1'='1' --",
        "' OR 1=1 --",
        "admin' OR '1'='1' --"
    ]

    for payload in payloads:

        assert secure_login(payload, "randompassword") == False
