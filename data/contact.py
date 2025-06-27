import json
from pathlib import Path
from typing import Dict, List
from filelock import FileLock

DATA_DIR = Path(__file__).resolve().parent
DATA_FILE = DATA_DIR / "contacts.json"
LOCK_FILE = DATA_FILE.with_suffix(".lock")

DATA_DIR.mkdir(parents=True, exist_ok=True)
lock = FileLock(str(LOCK_FILE))


def _load() -> List[Dict[str, str]]:
    with lock:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []


def _save(data: List[Dict[str, str]]) -> None:
    with lock:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


def add_contact(entry: Dict[str, str]) -> Dict[str, str]:
    data = _load()
    data.append(entry)
    _save(data)
    return entry


def read_all() -> List[Dict[str, str]]:
    return _load()
