from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'vulnerable_secret_key'  # Intentionally weak for testing

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  email TEXT)''')
    # Add test users
    c.execute("INSERT OR IGNORE INTO users (username, password, email) VALUES (?, ?, ?)",
             ('admin', 'admin123', 'admin@test.com'))
    c.execute("INSERT OR IGNORE INTO users (username, password, email) VALUES (?, ?, ?)",
              ('user1', 'pass123', 'user1@test.com'))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    data = request.form
    # Add your registration logic here
    return jsonify({"success": True})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    # Vulnerable: SQL Injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = c.execute(query).fetchone()
    conn.close()
    
    if result:
        session['user'] = {'id': result[0], 'username': result[1], 'email': result[3]}
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('profile.html')

@app.route('/edit-profile')
def edit_profile():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('edit-profile.html')

@app.route('/search')
def search():
    search_term = request.args.get('q', '')
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    # Vulnerable: SQL Injection
    query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%'"
    results = c.execute(query).fetchall()
    conn.close()
    
    users = [{'username': row[1], 'email': row[3]} for row in results]
    return jsonify(users)

@app.route('/upload', methods=['POST'])
def upload():
    if 'fileToUpload' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['fileToUpload']
    # Vulnerable: No file validation
    filename = secure_filename(file.filename)
    file.save(os.path.join('uploads', filename))
    
    return f"File uploaded successfully to: uploads/{filename}"

if __name__ == '__main__':
    init_db()
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)  # Vulnerable: Debug mode enabled 