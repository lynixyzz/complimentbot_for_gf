"""Хендлеры Telegram: эмоции коти, админ-панель, глобальная блокировка чужих."""
import functools

from telebot import types, util

from config import ADMIN_IDS, ALLOWED_IDS, WEBAPP_URL, load_state, update_state
from content import BUTTON_TO_CATEGORY, CATEGORIES, phrase_of_day, reply_for

DENIED = "Отказано! Вы не котя!"
_pending_geo: set[int] = set()  # админы, от которых ждём геолокацию


def is_allowed(uid: int) -> bool:
    return uid in ALLOWED_IDS or uid in ADMIN_IDS


def is_admin(uid: int) -> bool:
    return uid in ADMIN_IDS


def guard(admin_only=False):
    """Блокируем любое взаимодействие, если пользователь не котя (или не админ)."""
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(message, *a, **k):
            uid = message.from_user.id
            ok = is_admin(uid) if admin_only else is_allowed(uid)
            if not ok:
                bot.send_message(message.chat.id, DENIED)
                return
            return fn(message, *a, **k)
        return wrapper
    return deco


def build_keyboard() -> types.ReplyKeyboardMarkup:
    import random
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for cfg in CATEGORIES.values():
        kb.add(types.KeyboardButton(text=random.choice(cfg["buttons"])))
    if WEBAPP_URL:
        kb.add(types.KeyboardButton("Фраза дня 🔮", web_app=types.WebAppInfo(WEBAPP_URL)))
    return kb


def register(bot_instance) -> None:
    global bot
    bot = bot_instance

    @bot.message_handler(commands=["start"])
    @guard()
    def start(message):
        bot.send_message(message.chat.id, "Котя обнаружена!", reply_markup=build_keyboard())

    @bot.message_handler(func=lambda m: m.text in BUTTON_TO_CATEGORY)
    @guard()
    def emotion(message):
        category = BUTTON_TO_CATEGORY[message.text]
        kb = build_keyboard()
        bot.send_message(message.chat.id, reply_for(category), reply_markup=kb)
        for admin in ADMIN_IDS:
            try:
                bot.send_message(admin, CATEGORIES[category]["notify"])
            except Exception:
                pass

    # --- Админ-панель ---
    @bot.message_handler(commands=["admin"])
    @guard(admin_only=True)
    def admin(message):
        bot.send_message(message.chat.id, _admin_text(), reply_markup=_admin_keyboard())

    @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("adm:"))
    def admin_cb(call):
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, DENIED)
            return
        action = call.data.split(":", 1)[1]
        if action == "geo":
            _pending_geo.add(call.from_user.id)
            bot.send_message(call.message.chat.id,
                             "Пришли геолокацию 📍 или напиши координаты «широта,долгота».")
        elif action == "reset":
            seed = load_state().get("phrase_seed", 0) + 1
            update_state(phrase_seed=seed)
            bot.send_message(call.message.chat.id, f"Фраза дня сброшена ✅\n«{phrase_of_day()}»")
        bot.answer_callback_query(call.id)

    @bot.message_handler(content_types=["location"])
    @guard(admin_only=True)
    def set_location(message):
        if message.from_user.id not in _pending_geo:
            return
        _save_geo(message.chat.id, message.location.latitude, message.location.longitude)
        _pending_geo.discard(message.from_user.id)

    @bot.message_handler(func=lambda m: m.from_user.id in _pending_geo and m.text and "," in m.text)
    @guard(admin_only=True)
    def set_location_text(message):
        try:
            lat, lon = (float(x) for x in message.text.split(",", 1))
        except ValueError:
            bot.send_message(message.chat.id, "Не понял координаты. Формат: «55.75, 37.61».")
            return
        _save_geo(message.chat.id, lat, lon)
        _pending_geo.discard(message.from_user.id)

    def _save_geo(chat_id, lat, lon):
        update_state(lat=lat, lon=lon)
        bot.send_message(chat_id, f"Геолокация коти сохранена ✅\n{lat:.4f}, {lon:.4f}")

    # Fallback: любой другой контент — блокируем чужих, коте показываем клавиатуру.
    @bot.message_handler(func=lambda m: True, content_types=util.content_type_media)
    def fallback(message):
        if not is_allowed(message.from_user.id):
            bot.send_message(message.chat.id, DENIED)
            return
        bot.send_message(message.chat.id, "Котя обнаружена!", reply_markup=build_keyboard())


def _admin_text() -> str:
    state = load_state()
    geo = f"{state['lat']:.4f}, {state['lon']:.4f}" if "lat" in state else "не задана"
    return f"⚙️ Панель коти\nГеолокация: {geo}\nФраза дня: «{phrase_of_day()}»"


def _admin_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📍 Задать геолокацию", callback_data="adm:geo"))
    kb.add(types.InlineKeyboardButton("🔄 Сбросить фразу дня", callback_data="adm:reset"))
    return kb
