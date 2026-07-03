import json
import os
import threading
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(os.getenv("LEARNING_DATA_DIR", Path(__file__).parent / "data"))
LOCK = threading.Lock()

def valid_date(value=None):
    if value:
        try:
            return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            pass
    return datetime.now().strftime("%Y-%m-%d")

def save_record(record):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    path = DATA_DIR / f"{now:%Y-%m-%d}.json"
    item = {"time": now.isoformat(timespec="seconds"), **record}
    with LOCK:
        try:
            records = json.loads(path.read_text("utf-8")) if path.exists() else []
        except (OSError, json.JSONDecodeError):
            records = []
        records.append(item)
        path.write_text(json.dumps(records, ensure_ascii=False, indent=2), "utf-8")

def get_records(date=None):
    path = DATA_DIR / f"{valid_date(date)}.json"
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
