import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".lc-guard" / "config.json"


def get_username() -> str | None:
    try:
        return json.loads(CONFIG_PATH.read_text()).get("username")
    except Exception:
        return None


def set_username(username: str) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    try:
        data = json.loads(CONFIG_PATH.read_text())
    except Exception:
        pass
    data["username"] = username
    CONFIG_PATH.write_text(json.dumps(data, indent=2))
