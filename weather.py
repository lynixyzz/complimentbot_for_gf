"""Прогноз WeatherAPI.com: за день предупреждаем котю о дожде/грозе цитатой из data/weather.json."""
import threading
import time
from datetime import date

import requests

from config import ALLOWED_IDS, WEATHERAPI_KEY, load_state, update_state
from content import weather_quote

CHECK_EVERY = 3 * 3600  # раз в 3 часа проверяем прогноз на завтра


def categorize(condition: str | None) -> str | None:
    """Текст погоды WeatherAPI -> ключ плохой погоды ('thunderstorm'|'rain'|'snow') или None."""
    if not condition:
        return None
    c = condition.lower()
    if "thunder" in c or "hail" in c:
        return "thunderstorm"
    if "snow" in c or "sleet" in c or "blizzard" in c or "pellet" in c:
        return "snow"
    if "rain" in c or "shower" in c or "drizzle" in c:
        return "rain"
    return None


def tomorrow_condition(lat: float, lon: float) -> str | None:
    """Текст условия на завтра от WeatherAPI.com forecast, либо None при ошибке."""
    try:
        resp = requests.get(
            "https://api.weatherapi.com/v1/forecast.json",
            params={"key": WEATHERAPI_KEY, "q": f"{lat},{lon}", "days": 2},
            timeout=15,
        )
        resp.raise_for_status()
        days = resp.json().get("forecast", {}).get("forecastday", [])
        if len(days) < 2:
            return None
        return days[1].get("day", {}).get("condition", {}).get("text")
    except (requests.RequestException, ValueError, KeyError):
        return None


def check_once(bot) -> str | None:
    """Одна проверка: если завтра плохо и сегодня ещё не предупреждали — шлём цитату котям."""
    state = load_state()
    lat, lon = state.get("lat"), state.get("lon")
    if not (WEATHERAPI_KEY and lat is not None and lon is not None):
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
