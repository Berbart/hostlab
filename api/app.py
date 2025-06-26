from flask import Flask, jsonify, request
import markdown
from data import store

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

if __name__ == '__main__':
    app.run(debug=True)
