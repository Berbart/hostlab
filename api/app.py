import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
import markdown

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1MB

ALLOWED_EXTENSIONS = {"txt", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename: str) -> bool:
    """Check if the filename has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

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
