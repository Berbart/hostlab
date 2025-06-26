from flask import Flask, jsonify, request, send_from_directory, abort
import markdown
import os

app = Flask(__name__, static_folder='../public', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

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

if __name__ == '__main__':
    app.run(debug=True)
