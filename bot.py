"""Точка входа: бот-компаньон для коти. Комплименты, поддержка, погода, веб-апп «фраза дня»."""
import telebot

import weather
import server
from config import ALLOWED_IDS, ADMIN_IDS, BOT_TOKEN, WEBAPP_URL
from handlers import register


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("Укажите BOT_TOKEN в переменных окружения.")
    if not ALLOWED_IDS and not ADMIN_IDS:
        raise RuntimeError("Укажите ALLOWED_USERS (и/или ADMIN_IDS) в переменных окружения.")

    bot = telebot.TeleBot(BOT_TOKEN)
    register(bot)
    weather.start(bot)
    if WEBAPP_URL:
        server.start()
    bot.infinity_polling(timeout=10, long_polling_timeout=10)


if __name__ == "__main__":
    main()
