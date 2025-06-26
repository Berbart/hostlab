from flask import Flask, jsonify, request
import markdown
import json
import os

STATE_FILE = os.path.join(os.path.dirname(__file__), 'chess_state.json')

DEFAULT_BOARD = [
    ["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"]
]

app = Flask(__name__)

@app.route('/api/ping')
def ping():
    return jsonify({'message': 'pong'})

@app.route('/api/info')
def info():
    return jsonify({'project': 'Codex Playground', 'status': 'development'})

@app.route('/api/render', methods=['POST'])
def render_markdown():
    data = request.get_json() or {}
    text = data.get('text')
    if not text:
        return jsonify({'error': 'no text provided'}), 400
    html = markdown.markdown(text)
    return jsonify({'html': html})


def load_state():
    if not os.path.exists(STATE_FILE):
        return {'board': DEFAULT_BOARD, 'turn': 'white'}
    with open(STATE_FILE, 'r') as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)


@app.route('/api/chess', methods=['GET', 'POST'])
def chess_state():
    if request.method == 'GET':
        return jsonify(load_state())
    data = request.get_json() or {}
    board = data.get('board')
    turn = data.get('turn')
    if board is None or turn not in ('white', 'black'):
        return jsonify({'error': 'invalid state'}), 400
    save_state({'board': board, 'turn': turn})
    return jsonify({'status': 'saved'})

if __name__ == '__main__':
    app.run(debug=True)
