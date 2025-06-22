'''
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='')

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/calculate', methods=['POST'])

def calculate():
    data = request.json
    num1 = data.get('num1')
    num2 = data.get('num2')
    operator = data.get('operator')

    if operator == 'add':
        result = num1 + num2
    elif operator == 'subtract':
        result = num1 - num2
    elif operator == 'multiply':
        result = num1 * num2
    elif operator == 'divide':
        if num2 != 0:
            result = num1 / num2
        else:
            return jsonify({'error': 'Division by zero'}), 400
    else:
        return jsonify({'error': 'Invalid operator'}), 400

    return jsonify({'result': result})



if __name__ == '__main__':
    app.run(debug=True, port = 5001)
'''

from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from datetime import datetime

app = Flask(__name__, static_folder='')

DATABASE = 'calculate_history.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    num1 = data.get('num1')
    num2 = data.get('num2')
    operator = data.get('operator')

    try:
        if operator == 'add':
            result = num1 + num2
        elif operator == 'subtract':
            result = num1 - num2
        elif operator == 'multiply':
            result = num1 * num2
        elif operator == 'divide':
            if num2 != 0:
                result = num1 / num2
            else:
                return jsonify({'error': 'Division by zero'}), 400
        else:
            return jsonify({'error': 'Invalid operator'}), 400

        save_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = get_db_connection()
        conn.execute('INSERT INTO h (SaveTime, Data1, CalcType, Data2, Result) VALUES (?, ?, ?, ?, ?)',
                     (save_time, num1, operator, num2, result))
        conn.commit()
        conn.close()

        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def history():
    conn = get_db_connection()
    history = conn.execute('SELECT * FROM h').fetchall()
    conn.close()
    return jsonify([dict(row) for row in history])

@app.route('/history/<int:id>', methods=['GET'])
def get_history(id):
    conn = get_db_connection()
    history = conn.execute('SELECT * FROM h WHERE id = ?', (id,)).fetchone()
    conn.close()
    if history:
        return jsonify(dict(history))
    else:
        return jsonify({'error': 'Record not found'}), 404

@app.route('/history/first', methods=['GET'])
def get_first_history():
    conn = get_db_connection()
    history = conn.execute('SELECT * FROM h ORDER BY id ASC LIMIT 1').fetchone()
    conn.close()
    if history:
        return jsonify(dict(history))
    else:
        return jsonify({'error': 'No records found'}), 404

@app.route('/history/last', methods=['GET'])
def get_last_history():
    conn = get_db_connection()
    history = conn.execute('SELECT * FROM h ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()
    if history:
        return jsonify(dict(history))
    else:
        return jsonify({'error': 'No records found'}), 404

@app.route('/history/next/<int:id>', methods=['GET'])
def get_next_history(id):
    conn = get_db_connection()
    history = conn.execute('SELECT * FROM h WHERE id > ? ORDER BY id ASC LIMIT 1', (id,)).fetchone()
    conn.close()
    if history:
        return jsonify(dict(history))
    else:
        return jsonify({'error': 'No next record found'}), 404

@app.route('/history/prev/<int:id>', methods=['GET'])
def get_prev_history(id):
    conn = get_db_connection()
    history = conn.execute('SELECT * FROM h WHERE id < ? ORDER BY id DESC LIMIT 1', (id,)).fetchone()
    conn.close()
    if history:
        return jsonify(dict(history))
    else:
        return jsonify({'error': 'No previous record found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5002)