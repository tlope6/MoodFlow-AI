import json
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime

HISTORY_PATH = Path("data/history/sessions.json")

def append_history(entry: Dict[str, Any]) -> None:
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    data: List[Dict[str, Any]] = []
    if HISTORY_PATH.exists():
        try:
            data = json.loads(HISTORY_PATH.read_text())
        except Exception:
            data = []

    entry = dict(entry)
    entry["timestamp"] = datetime.utcnow().isoformat() + "Z"
    data.append(entry)

    HISTORY_PATH.write_text(json.dumps(data, indent=2))

def read_history() -> List[Dict[str, Any]]:
    if not HISTORY_PATH.exists():
        return []
    try:
        return json.loads(HISTORY_PATH.read_text())
    except Exception:
        return []
