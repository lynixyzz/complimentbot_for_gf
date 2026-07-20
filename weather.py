"""Прогноз Yandex Weather: за день предупреждаем котю о дожде/грозе цитатой из data/weather.json."""
import threading
import time
from datetime import date

import requests

from config import ALLOWED_IDS, YANDEX_WEATHER_KEY, load_state, update_state
from content import weather_quote

CHECK_EVERY = 3 * 3600  # раз в 3 часа проверяем прогноз на завтра

# Условие Yandex -> категория плохой погоды (ключ в data/weather.json). Остальное = хорошо.
_BAD = {
    "thunderstorm": ("thunderstorm", "hail"),
    "rain": ("rain", "showers", "drizzle", "wet-snow"),
    "snow": ("snow", "hail", "sleet"),
}


def categorize(condition: str | None) -> str | None:
    """Возвращает ключ плохой погоды ('thunderstorm'|'rain'|'snow') или None если погода нормальная."""
    if not condition:
        return None
    c = condition.lower()
    if "thunderstorm" in c or "hail" in c:
        return "thunderstorm"
    if "snow" in c or "sleet" in c:
        return "snow"
    if "rain" in c or "shower" in c or "drizzle" in c:
        return "rain"
    return None


def tomorrow_condition(lat: float, lon: float) -> str | None:
    """Условие погоды на завтра (день) от Yandex Weather API, либо None при ошибке."""
    try:
        resp = requests.get(
            "https://api.weather.yandex.ru/v2/forecast",
            params={"lat": lat, "lon": lon, "limit": 2, "hours": "false"},
            headers={"X-Yandex-API-Key": YANDEX_WEATHER_KEY},
            timeout=15,
        )
        resp.raise_for_status()
        forecasts = resp.json().get("forecasts", [])
        if len(forecasts) < 2:
            return None
        return forecasts[1].get("parts", {}).get("day", {}).get("condition")
    except (requests.RequestException, ValueError, KeyError):
        return None


def check_once(bot) -> str | None:
    """Одна проверка: если завтра плохо и сегодня ещё не предупреждали — шлём цитату котям."""
    state = load_state()
    lat, lon = state.get("lat"), state.get("lon")
    if not (YANDEX_WEATHER_KEY and lat is not None and lon is not None):
        return None

    category = categorize(tomorrow_condition(lat, lon))
    if not category:
        return None

    today = date.today().isoformat()
    if state.get("last_weather_warn") == today:
        return category  # уже предупредили сегодня

    quote = weather_quote(category)
    for uid in ALLOWED_IDS:
        try:
            bot.send_message(uid, quote)
        except Exception:
            pass
    update_state(last_weather_warn=today)
    return category


def start(bot) -> None:
    def loop():
        while True:
            try:
                check_once(bot)
            except Exception:
                pass
            time.sleep(CHECK_EVERY)

    threading.Thread(target=loop, daemon=True, name="weather").start()
