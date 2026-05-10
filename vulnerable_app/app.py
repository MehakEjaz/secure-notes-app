from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
# Create database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note TEXT
    )
    ''')
    # default admin user
    cursor.execute(
        "INSERT INTO users (username, password) VALUES ('admin', 'admin123')"
    )

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Notes App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body class="bg-light">

<div class="container mt-5">

    <div class="text-center mb-4">
        <h1 class="text-danger">⚠ Vulnerable Secure Notes App</h1>
        <p class="text-muted">CR-22026 & CR-22001 - Security Testing Version</p>
    </div>

    <div class="row">

        <!-- LOGIN CARD -->
        <div class="col-md-4">
            <div class="card shadow">
                <div class="card-header bg-danger text-white">Login</div>
                <div class="card-body">
                    <form method="POST" action="/login">
                        <input class="form-control mb-2" name="username" placeholder="Username">
                        <input class="form-control mb-2" name="password" placeholder="Password">
                        <button class="btn btn-danger w-100">Login</button>
                    </form>
                </div>
            </div>
        </div>

        <!-- NOTE CARD -->
        <div class="col-md-4">
            <div class="card shadow">
                <div class="card-header bg-warning">Add Note</div>
                <div class="card-body">
                    <form method="POST" action="/add_note">
                        <input class="form-control mb-2" name="note" placeholder="Write note">
                        <button class="btn btn-warning w-100">Save</button>
                    </form>
                </div>
            </div>
        </div>

        <!-- SEARCH CARD -->
        <div class="col-md-4">
            <div class="card shadow">
                <div class="card-header bg-info text-white">Search Notes</div>
                <div class="card-body">
                    <form method="GET" action="/search">
                        <input class="form-control mb-2" name="query" placeholder="Search">
                        <button class="btn btn-info w-100">Search</button>
                    </form>
                </div>
            </div>
        </div>

    </div>

</div>

</body>
</html>
""")

# SQL Injection Vulnerability
@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # INTENTIONALLY VULNERABLE

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    result = cursor.execute(query).fetchone()

    conn.close()

    if result:

        return render_template_string("""
        <!DOCTYPE html>
<html>

<head>
    <title>Vulnerable Dashboard</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body class="bg-light">

<div class="container mt-5">

    <div class="card shadow-lg border-success">

        <div class="card-header bg-success text-white">
            Vulnerable Dashboard
        </div>

        <div class="card-body text-center">

            <h1 class="text-success">
                ✅ Login Successful
            </h1>

            <p class="lead">
                Welcome, {{ username }}
            </p>

            <div class="alert alert-warning mt-4">

                <h4>Known Vulnerabilities</h4>

                <hr>

                • SQL Injection<br>
                • Cross-Site Scripting (XSS)<br>
                • Weak Password Storage

            </div>

            <div class="mt-4">

                <a href="/" class="btn btn-success">
                    Logout
                </a>

            </div>

        </div>

    </div>

</div>

</body>
</html>
""", username=username)

    else:

        return render_template_string("""
        <!DOCTYPE html>
        <html>

        <head>
            <title>Login Failed</title>

            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>

        <body class="bg-light">

        <div class="container mt-5">

            <div class="alert alert-danger shadow text-center">

                <h2>❌ Login Failed</h2>

                <p>
                    Invalid username or password.
                </p>

                <a href="/" class="btn btn-dark">
                    Try Again
                </a>

            </div>

        </div>

        </body>
        </html>
        """)

# XSS Vulnerability
@app.route('/add_note', methods=['POST'])
def add_note():

    note = request.form['note']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Safe insertion so payloads store properly
    # BUT output rendering below is still vulnerable to XSS
    cursor.execute(
        "INSERT INTO notes (note) VALUES (?)",
        (note,)
    )

    conn.commit()
    conn.close()

    # INTENTIONALLY VULNERABLE OUTPUT
    return render_template_string("""

    <!DOCTYPE html>
    <html>

    <head>
        <title>XSS Vulnerability Demo</title>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-light">

    <div class="container mt-5">

        <div class="card shadow-lg border-warning">

            <div class="card-header bg-warning">
                XSS Demonstration
            </div>

            <div class="card-body text-center">

                <h1 class="text-warning">
                    ⚠ Note Saved
                </h1>

                <p class="lead">
                    User input rendered directly without sanitization.
                </p>

                <div class="alert alert-danger">

                    <h5>Rendered Output:</h5>

                    <hr>

                    <!-- INTENTIONALLY VULNERABLE -->
                    """ + note + """

                </div>

                <p class="text-muted">
                    This demonstrates a Cross-Site Scripting (XSS) vulnerability.
                </p>

                <a href="/" class="btn btn-warning">
                    Back Home
                </a>

            </div>

        </div>

    </div>

    </body>
    </html>

    """)


# Vulnerable Search
@app.route('/search')
def search():

    query = request.args.get('query')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # INTENTIONALLY VULNERABLE

    sql = f"SELECT * FROM notes WHERE note LIKE '%{query}%'"

    results = cursor.execute(sql).fetchall()

    conn.close()

    return render_template_string("""

    <!DOCTYPE html>
    <html>

    <head>
        <title>Search Results</title>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-light">

    <div class="container mt-5">

        <div class="card shadow-lg border-info">

            <div class="card-header bg-info text-white">
                Vulnerable Search Results
            </div>

            <div class="card-body">

                <h2 class="mb-4">
                    🔎 Search Query:
                    <span class="text-primary">{{ query }}</span>
                </h2>

                <div class="alert alert-warning">

                    <strong>Warning:</strong>
                    This search functionality is vulnerable to SQL Injection.

                </div>

                <table class="table table-bordered table-hover">

                    <thead class="table-dark">

                        <tr>
                            <th>ID</th>
                            <th>Note</th>
                        </tr>

                    </thead>

                    <tbody>

                        {% for row in results %}

                        <tr>
                            <td>{{ row[0] }}</td>
                            <td>{{ row[1] }}</td>
                        </tr>

                        {% endfor %}

                    </tbody>

                </table>

                <a href="/" class="btn btn-info text-white">
                    Back Home
                </a>

            </div>

        </div>

    </div>

    </body>
    </html>

    """, query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)

