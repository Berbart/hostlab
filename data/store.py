import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from filelock import FileLock

DATA_DIR = Path(__file__).resolve().parent
DATA_FILE = DATA_DIR / "store.json"
LOCK_FILE = DATA_FILE.with_suffix(".lock")

# ensure directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

lock = FileLock(str(LOCK_FILE))


def _load_data() -> List[Dict[str, Any]]:
    with lock:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []


def _save_data(data: List[Dict[str, Any]]) -> None:
    with lock:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


def read_all() -> List[Dict[str, Any]]:
    return _load_data()


def get_entry(entry_id: int) -> Optional[Dict[str, Any]]:
    data = _load_data()
    for entry in data:
        if entry.get("id") == entry_id:
            return entry
    return None


def add_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    data = _load_data()
    next_id = max((item.get("id", 0) for item in data), default=0) + 1
    entry_with_id = {"id": next_id, **entry}
    data.append(entry_with_id)
    _save_data(data)
    return entry_with_id


def update_entry(entry_id: int, entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    data = _load_data()
    for idx, item in enumerate(data):
        if item.get("id") == entry_id:
            data[idx] = {"id": entry_id, **entry}
            _save_data(data)
            return data[idx]
    return None


def delete_entry(entry_id: int) -> bool:
    data = _load_data()
    for idx, item in enumerate(data):
        if item.get("id") == entry_id:
            data.pop(idx)
            _save_data(data)
            return True
    return False
