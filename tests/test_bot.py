"""Проверки чистой логики: парсинг id, фраза дня, категории погоды, доступ."""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import parse_ids  # noqa: E402
from weather import categorize  # noqa: E402
import content  # noqa: E402


def test_parse_ids():
    assert parse_ids("1, 2 ,3") == [1, 2, 3]
    assert parse_ids("7087783397") == [7087783397]
    assert parse_ids("") == []
    assert parse_ids(None) == []
    assert parse_ids(" ") == []


def test_categorize():
    # тексты условий weatherapi.com
    assert categorize("Patchy rain possible") == "rain"
    assert categorize("Moderate rain") == "rain"
    assert categorize("Patchy light drizzle") == "rain"
    assert categorize("Thundery outbreaks possible") == "thunderstorm"
    assert categorize("Patchy light rain with thunder") == "thunderstorm"
    assert categorize("Heavy snow") == "snow"
    assert categorize("Blizzard") == "snow"
    assert categorize("Ice pellets") == "snow"
    assert categorize("Sunny") is None
    assert categorize("Partly cloudy") is None
    assert categorize(None) is None


def test_phrase_of_day_deterministic_and_resettable():
    d = date(2026, 7, 21)
    assert content.phrase_of_day(d, seed=0) == content.phrase_of_day(d, seed=0)
    # сброс (seed++) меняет фразу дня хотя бы на одном из первых сидов
    base = content.phrase_of_day(d, seed=0)
    assert any(content.phrase_of_day(d, seed=s) != base for s in range(1, 5))


def test_button_to_category_covers_all():
    for key, cfg in content.CATEGORIES.items():
        for btn in cfg["buttons"]:
            assert content.BUTTON_TO_CATEGORY[btn] == key


def test_reply_falls_back_when_empty(monkeypatch):
    monkeypatch.setitem(content.QUOTES, "compliments", [])
    assert content.reply_for("compliments") == content.WAITING
