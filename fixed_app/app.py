from flask import Flask, request, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('secure.db')
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

    hashed = generate_password_hash("admin123")

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", hashed)
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

    <title>Secure Notes App</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

</head>

<body class="bg-light">

<div class="container mt-5">

    <div class="text-center mb-4">

        <h1 class="text-success">
            🔒 Secure Notes App
        </h1>

        <p class="text-muted">
            Fixed Version - Secure Coding Practices Applied
        </p>

    </div>

    <div class="row">

        <!-- LOGIN -->
        <div class="col-md-6">

            <div class="card shadow">

                <div class="card-header bg-success text-white">
                    Secure Login
                </div>

                <div class="card-body">

                    <form method="POST" action="/login">

                        <input class="form-control mb-3"
                               name="username"
                               placeholder="Username">

                        <input class="form-control mb-3"
                               name="password"
                               placeholder="Password">

                        <button class="btn btn-success w-100">
                            Login
                        </button>

                    </form>

                </div>

            </div>

        </div>

        <!-- NOTES -->
        <div class="col-md-6">

            <div class="card shadow">

                <div class="card-header bg-primary text-white">
                    Secure Notes
                </div>

                <div class="card-body">

                    <form method="POST" action="/add_note">

                        <input class="form-control mb-3"
                               name="note"
                               placeholder="Write secure note">

                        <button class="btn btn-primary w-100">
                            Save Note
                        </button>

                    </form>
                        <hr>

    <form method="GET" action="/search">

        <input class="form-control mb-3"
               name="query"
               placeholder="Search notes">

        <button class="btn btn-outline-success w-100">
            Search
        </button>

    </form>

                </div>

            </div>

        </div>

    </div>

</div>

</body>

</html>

""")

@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('secure.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user[2], password):

        return render_template_string("""

        <!DOCTYPE html>
        <html>

        <head>

            <title>Secure Dashboard</title>

            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

        </head>

        <body class="bg-light">

        <div class="container mt-5">

            <div class="card shadow-lg border-success">

                <div class="card-header bg-success text-white">
                    Secure Dashboard
                </div>

                <div class="card-body text-center">

                    <h1 class="text-success">
                        🔒 Secure Login Successful
                    </h1>

                    <p class="lead">
                        Welcome, {{ username }}
                    </p>

                    <div class="alert alert-success mt-4">

                        <h4>Security Protections Enabled</h4>

                        <hr>

                        ✔ Parameterized Queries<br>
                        ✔ Password Hashing<br>
                        ✔ Output Escaping<br>
                        ✔ Secure Input Handling

                    </div>

                    <a href="/" class="btn btn-success">
                        Logout
                    </a>

                </div>

            </div>

        </div>

        </body>
        </html>

        """, username=username)

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
                Incorrect username or password.
            </p>

            <a href="/" class="btn btn-dark">
                Try Again
            </a>

        </div>

    </div>

    </body>
    </html>

    """)
@app.route('/add_note', methods=['POST'])
def add_note():

    note = escape(request.form['note'])

    conn = sqlite3.connect('secure.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (note) VALUES (?)",
        (note,)
    )

    conn.commit()
    conn.close()

    return render_template_string("""

    <!DOCTYPE html>
    <html>

    <head>

        <title>Secure Note Saved</title>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    </head>

    <body class="bg-light">

    <div class="container mt-5">

        <div class="card shadow-lg border-primary">

            <div class="card-header bg-primary text-white">
                Secure Note Storage
            </div>

            <div class="card-body text-center">

                <h1 class="text-primary">
                    🔒 Secure Note Saved
                </h1>

                <p class="lead">
                    Input was safely escaped before rendering.
                </p>

                <div class="alert alert-success">

                    <h5>Rendered Safe Output:</h5>

                    <hr>

                    {{ note }}

                </div>

                <p class="text-muted">
                    This prevents Cross-Site Scripting (XSS) attacks.
                </p>

                <a href="/" class="btn btn-primary">
                    Back Home
                </a>

            </div>

        </div>

    </div>

    </body>
    </html>

    """, note=note)
@app.route('/search')
def search():

    query = request.args.get('query', '')

    conn = sqlite3.connect('secure.db')
    cursor = conn.cursor()

    # ✅ FIXED: parameterized query (prevents SQL injection)
    cursor.execute(
        "SELECT * FROM notes WHERE note LIKE ?",
        ('%' + query + '%',)
    )

    results = cursor.fetchall()
    conn.close()

    return render_template_string("""
    <!DOCTYPE html>
    <html>

    <head>
        <title>Secure Search Results</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-light">

    <div class="container mt-5">

        <div class="card shadow-lg border-success">

            <div class="card-header bg-success text-white">
                Secure Search Results
            </div>

            <div class="card-body">

                <h2>
                    🔎 Search: {{ query }}
                </h2>

                <div class="alert alert-success">
                    This version is protected against SQL Injection using parameterized queries.
                </div>

                <table class="table table-bordered">

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

                <a href="/" class="btn btn-success">
                    Back Home
                </a>

            </div>

        </div>

    </div>

    </body>
    </html>
    """, query=escape(query), results=results)
if __name__ == '__main__':
    app.run(debug=True, port=5001)
