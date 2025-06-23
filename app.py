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