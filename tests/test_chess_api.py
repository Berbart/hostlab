import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.app import app, DEFAULT_BOARD, STATE_FILE
import json


def test_chess_get(tmp_path, monkeypatch):
    tmp_file = tmp_path / 'state.json'
    monkeypatch.setattr('api.app.STATE_FILE', str(tmp_file))
    client = app.test_client()
    res = client.get('/api/chess')
    assert res.status_code == 200
    data = res.get_json()
    assert data['board'] == DEFAULT_BOARD
    assert data['turn'] == 'white'


def test_chess_post(tmp_path, monkeypatch):
    tmp_file = tmp_path / 'state.json'
    monkeypatch.setattr('api.app.STATE_FILE', str(tmp_file))
    client = app.test_client()
    board = [['' for _ in range(8)] for _ in range(8)]
    payload = {'board': board, 'turn': 'black'}
    res = client.post('/api/chess', json=payload)
    assert res.status_code == 200
    assert res.get_json() == {'status': 'saved'}
    with open(tmp_file) as f:
        saved = json.load(f)
    assert saved == payload
