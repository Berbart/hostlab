from api.app import app
import io
import os


def login(client, username="admin", password="secret"):
    res = client.post(
        "/api/login", json={"username": username, "password": password}
    )
    assert res.status_code == 200
    return res.get_json()["token"]

def test_ping():
    client = app.test_client()
    res = client.get('/api/ping')
    assert res.status_code == 200
    assert res.get_json() == {'message': 'pong'}


def test_login_success():
    client = app.test_client()
    res = client.post('/api/login', json={'username': 'admin', 'password': 'secret'})
    assert res.status_code == 200
    assert 'token' in res.get_json()

def test_info():
    client = app.test_client()
    token = login(client)
    res = client.get('/api/info', headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 200
    assert res.get_json() == {'project': 'Codex Playground', 'status': 'development'}

def test_render_markdown():
    client = app.test_client()
    token = login(client)
    res = client.post('/api/render', json={'text': '# Title'}, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 200
    assert res.get_json() == {'html': '<h1>Title</h1>'}

def test_render_markdown_no_text():
    client = app.test_client()
    token = login(client)
    res = client.post('/api/render', json={}, headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 400

def test_login_failure():
    client = app.test_client()
    res = client.post('/api/login', json={'username': 'admin', 'password': 'wrong'})
    assert res.status_code == 401


def test_access_without_token():
    client = app.test_client()
    res = client.get('/api/info')
    assert res.status_code == 401


def test_render_requires_token():
    client = app.test_client()
    res = client.post('/api/render', json={'text': '# Title'})
    assert res.status_code == 401

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

