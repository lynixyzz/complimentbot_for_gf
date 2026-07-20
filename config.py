"""Настройки из окружения + постоянное состояние (гео, сид фразы, дата предупреждения о погоде)."""
import json
import os
import threading
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STATE_FILE = BASE_DIR / "state.json"


def _load_dotenv() -> None:
    """Подхватываем .env рядом с ботом, если он есть (без зависимостей)."""
    env = BASE_DIR / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def parse_ids(raw: str | None) -> list[int]:
    """'1, 2 ,3' -> [1, 2, 3]. Пустое/None -> []."""
    if not raw:
        return []
    return [int(x) for x in (p.strip() for p in raw.split(",")) if x]


_load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_IDS = parse_ids(os.getenv("ALLOWED_USERS"))
ADMIN_IDS = parse_ids(os.getenv("ADMIN_IDS"))
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")
WEBAPP_URL = os.getenv("WEBAPP_URL")
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT", "8080"))

_lock = threading.Lock()


def load_state() -> dict:
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_state(**changes) -> dict:
    """Атомарно (в пределах процесса) обновляем и сохраняем состояние."""
    with _lock:
        state = load_state()
        state.update(changes)
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        return state
