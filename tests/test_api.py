from api.app import app
import io
import os

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


def test_file_upload_and_download(tmp_path):
    app.config['UPLOAD_FOLDER'] = str(tmp_path)
    client = app.test_client()
    data = {'file': (io.BytesIO(b'hello'), 'hello.txt')}
    res = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert res.status_code == 201
    assert res.get_json() == {'filename': 'hello.txt'}
    assert (tmp_path / 'hello.txt').exists()

    res = client.get('/api/files/hello.txt')
    assert res.status_code == 200
    assert res.data == b'hello'


def test_upload_invalid_type(tmp_path):
    app.config['UPLOAD_FOLDER'] = str(tmp_path)
    client = app.test_client()
    data = {'file': (io.BytesIO(b'bad'), 'bad.exe')}
    res = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert res.status_code == 400

