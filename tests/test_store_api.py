import json
from api.app import app
from data import store
from filelock import FileLock
import pytest


@pytest.fixture(autouse=True)
def temp_store(tmp_path, monkeypatch):
    data_file = tmp_path / "store.json"
    lock_file = data_file.with_suffix(".lock")
    monkeypatch.setattr(store, "DATA_FILE", data_file, raising=False)
    monkeypatch.setattr(store, "LOCK_FILE", lock_file, raising=False)
    monkeypatch.setattr(store, "lock", FileLock(str(lock_file)), raising=False)
    yield
    if lock_file.exists():
        lock_file.unlink()
    if data_file.exists():
        data_file.unlink()


def test_store_crud():
    client = app.test_client()

    res = client.get('/api/store')
    assert res.status_code == 200
    assert res.get_json() == []

    res = client.post('/api/store', json={'name': 'Alice'})
    assert res.status_code == 201
    entry = res.get_json()
    assert entry['id'] == 1
    assert entry['name'] == 'Alice'

    res = client.get(f"/api/store/{entry['id']}")
    assert res.status_code == 200
    assert res.get_json()['name'] == 'Alice'

    res = client.put(f"/api/store/{entry['id']}", json={'name': 'Bob'})
    assert res.status_code == 200
    assert res.get_json()['name'] == 'Bob'

    res = client.delete(f"/api/store/{entry['id']}")
    assert res.status_code == 200
    assert res.get_json() == {'status': 'deleted'}

    res = client.get(f"/api/store/{entry['id']}")
    assert res.status_code == 404
