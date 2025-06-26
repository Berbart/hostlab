from flask import Flask, jsonify, request
import markdown
import secrets
from functools import wraps

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
