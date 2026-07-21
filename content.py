"""Загрузка фраз из data/*.json, категории кнопок, случайные выборки, фраза дня."""
import hashlib
import json
import random
from datetime import date

from config import DATA_DIR, load_state

# Категории эмоций: ключ -> (файл с фразами, варианты кнопок, текст уведомления админам).
CATEGORIES = {
    "compliments": {
        "buttons": ['Комплиментик? 😼', 'Комплиментик? 👑', 'Комплиментик? ❤️‍🔥',
                    'Комплиментик? 🫦', 'Комплиментик? 💗', 'Комплиментик? 💞'],
        "notify": "котя хочет комплиментов...",
    },
    "motivation": {
        "buttons": ['Грустно? 😿', 'Грустно? 😓', 'Грустно? ☔️'],
        "notify": "котя чувствует себя грустно...",
    },
    "insecurity": {
        "buttons": ['Сомнения? 😕', 'Сомнения? 💭', 'Сомнения? 🤔'],
        "notify": "котя чувствует себя неуверенно...",
    },
    "alone": {
        "buttons": ['Одиноко? 😖', 'Одиноко? 💔', 'Одиноко? 🤧'],
        "notify": "котя чувствует себя одиноко...",
    },
    "tired": {
        "buttons": ['Устала? 😫', 'Устала? 🫩', 'Устала? 🤕'],
        "notify": "котя устала...",
    },
}
WAITING = "Подожди немножко, котя ❤️"


def _load_list(name: str) -> list:
    try:
        with open(DATA_DIR / f"{name}.json", encoding="utf-8") as f:
            loaded = json.load(f)
        return loaded if isinstance(loaded, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _load_dict(name: str) -> dict:
    try:
        with open(DATA_DIR / f"{name}.json", encoding="utf-8") as f:
            loaded = json.load(f)
        return loaded if isinstance(loaded, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


QUOTES = {name: _load_list(name) for name in CATEGORIES}
WEATHER_QUOTES = _load_dict("weather")
PHRASES = _load_list("phrases")

# Текст кнопки -> ключ категории.
BUTTON_TO_CATEGORY = {btn: key for key, cfg in CATEGORIES.items() for btn in cfg["buttons"]}


def reply_for(category: str) -> str:
    quotes = QUOTES.get(category) or []
    return random.choice(quotes) if quotes else WAITING


def weather_quote(category: str) -> str:
    quotes = WEATHER_QUOTES.get(category) or WEATHER_QUOTES.get("default") or []
    return random.choice(quotes) if quotes else "полгода плохая погода..."


def phrase_of_day(on: date | None = None, seed: int | None = None) -> str:
    """Детерминированная «фраза дня»: одна и та же за сутки, меняется при сбросе (seed++)."""
    if not PHRASES:
        return "Дыши. Ты справляешься лучше, чем думаешь."
    if on is None:
        on = date.today()
    if seed is None:
        seed = load_state().get("phrase_seed", 0)
    digest = hashlib.sha256(f"{on.isoformat()}:{seed}".encode()).hexdigest()
    return PHRASES[int(digest, 16) % len(PHRASES)]
