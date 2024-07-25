from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize the database
def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()

init_db()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    
    if not first_name or not last_name or not email:
        return jsonify({'success': False, 'message': 'Invalid input.'})

    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (first_name, last_name, email) VALUES (?, ?, ?)', (first_name, last_name, email))
            conn.commit()
        return jsonify({'success': True, 'message': 'User registered successfully.'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Email already exists.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT first_name, last_name, email FROM users')
    users = cursor.fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

if __name__ == '__main__':
    app.run(debug=True)
