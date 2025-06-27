import json
from api.app import app
from data import contact
from filelock import FileLock
import pytest


@pytest.fixture(autouse=True)
def temp_contact(tmp_path, monkeypatch):
    data_file = tmp_path / "contacts.json"
    lock_file = data_file.with_suffix(".lock")
    monkeypatch.setattr(contact, "DATA_FILE", data_file, raising=False)
    monkeypatch.setattr(contact, "LOCK_FILE", lock_file, raising=False)
    monkeypatch.setattr(contact, "lock", FileLock(str(lock_file)), raising=False)
    yield
    if lock_file.exists():
        lock_file.unlink()
    if data_file.exists():
        data_file.unlink()


def test_create_contact():
    client = app.test_client()
    payload = {"name": "Alice", "email": "alice@example.com", "message": "Hi"}
    res = client.post("/api/contact", json=payload)
    assert res.status_code == 201
    assert res.get_json() == {"status": "received"}
    assert contact.read_all() == [payload]


def test_contact_invalid():
    client = app.test_client()
    res = client.post("/api/contact", json={"name": "Bob"})
    assert res.status_code == 400
