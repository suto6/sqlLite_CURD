import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_path = "/home/sutapa/databases/sqlLite/test.db"

# Database setup
def init_db():
    conn = sqlite3.connect(DB_path)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Get all users from database
def get_users():
    conn = sqlite3.connect(DB_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()
    return users 

# Add user to database
def add_user(name, email, password):
    conn = sqlite3.connect(DB_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    conn.close()

# Update user in database (renamed this function)
def update_user_in_db(id, name, email, password):
    conn = sqlite3.connect(DB_path)
    cur = conn.cursor()
    cur.execute("UPDATE users SET name=?, email=?, password=? WHERE id=?", (name, email, password, id))
    conn.commit()
    conn.close()

# Delete user from database
def delete_user_from_db(id):
    conn = sqlite3.connect(DB_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()

# Home page
@app.route('/')
def index():
    users = get_users()
    return render_template('index.html', users=users)

# Add new user
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    add_user(name, email, password)
    return redirect(url_for('index'))

# Update user
@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        update_user_in_db(id, name, email, password)
        return redirect(url_for('index'))

    # Pre-fill form with current user data
    conn = sqlite3.connect(DB_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (id,))
    user = cur.fetchone()
    conn.close()
    return render_template('update_user.html', user=user)

# Delete user
@app.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
    delete_user_from_db(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
