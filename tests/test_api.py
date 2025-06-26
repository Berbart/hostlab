import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.app import app

def test_ping():
    client = app.test_client()
    res = client.get('/api/ping')
    assert res.status_code == 200
    assert res.get_json() == {'message': 'pong'}

def test_info():
    client = app.test_client()
    res = client.get('/api/info')
    assert res.status_code == 200
    assert res.get_json() == {'project': 'Codex Playground', 'status': 'development'}

def test_render_markdown():
    client = app.test_client()
    res = client.post('/api/render', json={'text': '# Title'})
    assert res.status_code == 200
    assert res.get_json() == {'html': '<h1>Title</h1>'}

def test_render_markdown_no_text():
    client = app.test_client()
    res = client.post('/api/render', json={})
    assert res.status_code == 400
