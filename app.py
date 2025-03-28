from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "super-secret-key"  # Vulnerable: Hardcoded secret key

# Database initialization
def init_db():
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  password TEXT,
                  email TEXT)''')
    
    # Add test data
    c.execute("INSERT OR IGNORE INTO users (username, password, email) VALUES (?, ?, ?)",
              ('admin', 'admin123', 'admin@test.com'))
    c.execute("INSERT OR IGNORE INTO users (username, password, email) VALUES (?, ?, ?)",
              ('user1', 'pass123', 'user1@test.com'))
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Vulnerable: SQL Injection possible
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    c.execute(query)
    user = c.fetchone()
    conn.close()
    
    if user:
        return jsonify({
            'success': True,
            'user': {
                'id': user[0],
                'username': user[1],
                'email': user[3]
            }
        })
    return jsonify({'success': False})

@app.route('/search')
def search():
    search_term = request.args.get('q', '')
    
    # Vulnerable: SQL Injection
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%'"
    c.execute(query)
    users = c.fetchall()
    conn.close()
    
    return jsonify([{
        'id': user[0],
        'username': user[1],
        'email': user[3]
    } for user in users])

@app.route('/upload', methods=['POST'])
def upload():
    if 'fileToUpload' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['fileToUpload']
    # Vulnerable: No file validation
    filename = secure_filename(file.filename)
    file.save(os.path.join('uploads', filename))
    
    return f"File uploaded successfully to: uploads/{filename}"

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/edit-profile')
def edit_profile():
    return render_template('edit-profile.html')

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)  # Vulnerable: Debug mode enabled 