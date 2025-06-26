from flask import Flask, jsonify, request, send_from_directory, abort
import markdown
import os

app = Flask(__name__, static_folder='../public', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

from pathlib import Path

from werkzeug.utils import secure_filename
import secrets
from functools import wraps
from data import store

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

import json

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
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1MB

ALLOWED_EXTENSIONS = {"txt", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename: str) -> bool:
    """Check if the filename has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Dummy user store and token storage
USERS = {"admin": "secret"}
TOKENS = {}


def login_required(f):
    """Simple decorator to require a valid token."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        token = None
        if auth.startswith("Bearer "):
            token = auth.split(" ", 1)[1]
        if not token:
            token = request.args.get("token")
        if not token or token not in TOKENS.values():
            return jsonify({"error": "unauthorized"}), 401
        return f(*args, **kwargs)

    return wrapper

@app.route('/api/ping')
def ping():
    return jsonify({'message': 'pong'})

@app.route('/api/info')
@login_required
def info():
    return jsonify({'project': 'Codex Playground', 'status': 'development'})

@app.route('/api/render', methods=['POST'])
@login_required
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

@app.route('/api/images')
def list_images():
    image_dir = os.path.join(app.static_folder, 'images')
    try:
        files = [f for f in os.listdir(image_dir) if not f.startswith('.')]
    except FileNotFoundError:
        files = []
    return jsonify(files)

@app.route('/articles/<name>')
def article(name):
    path = os.path.join('../content', f'{name}.md')
    if not os.path.exists(path):
        abort(404)
    with open(path, 'r') as f:
        html = markdown.markdown(f.read())
    return f"<html><body>{html}</body></html>"

@app.route('/api/login', methods=['POST'])
def login():
    """Dummy login returning a simple token."""
    data = request.get_json() or {}
    user = data.get("username")
    password = data.get("password")
    if USERS.get(user) != password:
        return jsonify({"error": "invalid credentials"}), 401
    token = secrets.token_hex(16)
    TOKENS[user] = token
    return jsonify({"token": token})
  
# Simple JSON store endpoints
@app.route('/api/store', methods=['GET'])
def list_entries():
    return jsonify(store.read_all())


@app.route('/api/store/<int:entry_id>', methods=['GET'])
def get_single_entry(entry_id):
    entry = store.get_entry(entry_id)
    if entry is None:
        return jsonify({'error': 'not found'}), 404
    return jsonify(entry)


@app.route('/api/store', methods=['POST'])
def create_entry():
    data = request.get_json() or {}
    if not isinstance(data, dict):
        return jsonify({'error': 'invalid data'}), 400
    new_entry = store.add_entry(data)
    return jsonify(new_entry), 201


@app.route('/api/store/<int:entry_id>', methods=['PUT'])
def update_single_entry(entry_id):
    data = request.get_json() or {}
    if not isinstance(data, dict):
        return jsonify({'error': 'invalid data'}), 400
    updated = store.update_entry(entry_id, data)
    if updated is None:
        return jsonify({'error': 'not found'}), 404
    return jsonify(updated)


@app.route('/api/store/<int:entry_id>', methods=['DELETE'])
def delete_single_entry(entry_id):
    if store.delete_entry(entry_id):
        return jsonify({'status': 'deleted'})
    return jsonify({'error': 'not found'}), 404

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads with basic validation."""
    if 'file' not in request.files:
        return jsonify({'error': 'no file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'no selected file'}), 400

    filename = secure_filename(file.filename)

    if not allowed_file(filename):
        return jsonify({'error': 'invalid file type'}), 400

    save_path = Path(app.config['UPLOAD_FOLDER']) / filename
    file.save(save_path)
    return jsonify({'filename': filename}), 201


@app.route('/api/files/<path:filename>')
def get_file(filename):
    """Serve a file from the upload directory."""
    safe_name = secure_filename(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], safe_name)

if __name__ == '__main__':
    app.run(debug=True)
