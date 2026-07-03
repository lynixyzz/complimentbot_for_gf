import os
import telebot
from telebot import types
import random
import json

'''

ПЕРЕМЕННЫЕ

'''
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
ALLOWED_IDS = []

compliments = []
motivation = []
insecurity = []
alone = []
tired = []

emojis_comp = ['Комплиментик? 😼', 'Комплиментик? 👑', 'Комплиментик? ❤️‍🔥', 'Комплиментик? 🫦', 'Комплиментик? 💗', 'Комплиментик? 💞']
emojis_sad = ['Грустно? 😿', 'Грустно? 😓', 'Грустно? ☔️']
emojis_alone = ['Одиноко? 😖', 'Одиноко? 💔', 'Одиноко? 🤧']
emojis_insecurity = ['Сомнения? 😕', 'Сомнения? 💭', 'Сомнения? 🤔']
emojis_tired = ['Устала? 😫', 'Устала? 🫩', 'Устала? 🤕']

'''

ПРОЧЕЕ

'''

try:
    with open('data/compliments.json', 'r', encoding='utf-8') as file:
        loaded = json.load(file)
        if isinstance(loaded, list):
            compliments = loaded
except (FileNotFoundError, json.JSONDecodeError):
    compliments = []

try:
    with open('data/motivation.json', 'r', encoding='utf-8') as file:
        loaded = json.load(file)
        if isinstance(loaded, list):
            motivation = loaded
except (FileNotFoundError, json.JSONDecodeError):
    motivation = []

try:
    with open('data/insecurity.json', 'r', encoding='utf-8') as file:
        loaded = json.load(file)
        if isinstance(loaded, list):
            insecurity = loaded
except (FileNotFoundError, json.JSONDecodeError):
    insecurity = []

try:
    with open('data/alone.json', 'r', encoding='utf-8') as file:
        loaded = json.load(file)
        if isinstance(loaded, list):
            alone = loaded
except (FileNotFoundError, json.JSONDecodeError):
    alone = []

try:
    with open('data/tired.json', 'r', encoding='utf-8') as file:
        loaded = json.load(file)
        if isinstance(loaded, list):
            tired = loaded
except (FileNotFoundError, json.JSONDecodeError):
    tired = []

if len(ALLOWED_IDS) == 0:
    raise RuntimeError(
        "Укажите ALLOWED_TELEGRAM_ID в переменных окружения перед запуском бота."
    )

'''

MESSAGE_HANDLER

'''

@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.id not in ALLOWED_IDS:
        bot.send_message(message.chat.id, "Отказано! Вы не котя!")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=emojis_comp[random.randrange(0, len(emojis_comp))]))
    keyboard.add(types.KeyboardButton(text=emojis_sad[random.randrange(0, len(emojis_sad))]))
    keyboard.add(types.KeyboardButton(text=emojis_insecurity[random.randrange(0, len(emojis_insecurity))]))
    keyboard.add(types.KeyboardButton(text=emojis_alone[random.randrange(0, len(emojis_alone))]))
    keyboard.add(types.KeyboardButton(text=emojis_tired[random.randrange(0, len(emojis_tired))]))

    bot.send_message(
        chat_id=message.chat.id,
        text="Котя обнаружена!",
        reply_markup=keyboard
    )

'''
КОМПЛИМЕНТЫ
'''

@bot.message_handler(func=lambda message: message.text in emojis_comp)
def send_compliment(message):
    if message.from_user.id not in ALLOWED_IDS:
        bot.send_message(message.chat.id, "Отказано! Вы не котя!")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=emojis_comp[random.randrange(0, len(emojis_comp))]))  # 1
    keyboard.add(types.KeyboardButton(text=emojis_sad[random.randrange(0, len(emojis_sad))]))  # 2
    keyboard.add(types.KeyboardButton(text=emojis_insecurity[random.randrange(0, len(emojis_insecurity))]))  # 3
    keyboard.add(types.KeyboardButton(text=emojis_alone[random.randrange(0, len(emojis_alone))]))  # 4
    keyboard.add(types.KeyboardButton(text=emojis_tired[random.randrange(0, len(emojis_tired))]))  # 5

    if compliments:
        bot.send_message(
            message.chat.id,
            compliments[random.randrange(0, len(compliments))],
            reply_markup=keyboard
        )
    else:
        bot.send_message(
            message.chat.id,
            "Подожди немножко, котя ❤️",
            reply_markup=keyboard
        )

    bot.send_message(
        chat_id=7087783397,
        text='котя хочет комплиментов...',
        reply_markup=keyboard
    )

'''
ГРУСТНО
'''

@bot.message_handler(func=lambda message: message.text in emojis_sad)
def send_motivation(message):
    if message.from_user.id not in ALLOWED_IDS:
        bot.send_message(message.chat.id, "Отказано! Вы не котя!")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=emojis_comp[random.randrange(0, len(emojis_comp))]))
    keyboard.add(types.KeyboardButton(text=emojis_sad[random.randrange(0, len(emojis_sad))]))
    keyboard.add(types.KeyboardButton(text=emojis_insecurity[random.randrange(0, len(emojis_insecurity))]))
    keyboard.add(types.KeyboardButton(text=emojis_alone[random.randrange(0, len(emojis_alone))]))
    keyboard.add(types.KeyboardButton(text=emojis_tired[random.randrange(0, len(emojis_tired))]))

    if motivation:
        bot.send_message(
            message.chat.id,
            motivation[random.randrange(0, len(motivation))],
            reply_markup=keyboard
        )
    else:
        bot.send_message(
            message.chat.id,
            "Подожди немножко, котя ❤️",
            reply_markup=keyboard
        )
    
    bot.send_message(
        chat_id=7087783397,
        text='котя чувствует себя грустно...',
        reply_markup=keyboard
    )

'''
СОМНЕНИЯ В СЕБЕ
'''

@bot.message_handler(func=lambda message: message.text in emojis_insecurity)
def send_insecurity(message):
    if message.from_user.id not in ALLOWED_IDS:
        bot.send_message(message.chat.id, "Отказано! Вы не котя!")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=emojis_comp[random.randrange(0, len(emojis_comp))]))
    keyboard.add(types.KeyboardButton(text=emojis_sad[random.randrange(0, len(emojis_sad))]))
    keyboard.add(types.KeyboardButton(text=emojis_insecurity[random.randrange(0, len(emojis_insecurity))]))
    keyboard.add(types.KeyboardButton(text=emojis_alone[random.randrange(0, len(emojis_alone))]))
    keyboard.add(types.KeyboardButton(text=emojis_tired[random.randrange(0, len(emojis_tired))]))

    if insecurity:
        bot.send_message(
            message.chat.id,
            insecurity[random.randrange(0, len(insecurity))],
            reply_markup=keyboard
        )
    else:
        bot.send_message(
            message.chat.id,
            "Подожди немножко, котя ❤️",
            reply_markup=keyboard
        )
    
    bot.send_message(
        chat_id=7087783397,
        text='котя чувствует себя неуверенно...',
        reply_markup=keyboard
    )

'''
ОДИНОКО
'''

@bot.message_handler(func=lambda message: message.text in emojis_alone)
def send_alone(message):
    if message.from_user.id not in ALLOWED_IDS:
        bot.send_message(message.chat.id, "Отказано! Вы не котя!")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=emojis_comp[random.randrange(0, len(emojis_comp))]))
    keyboard.add(types.KeyboardButton(text=emojis_sad[random.randrange(0, len(emojis_sad))]))
    keyboard.add(types.KeyboardButton(text=emojis_insecurity[random.randrange(0, len(emojis_insecurity))]))
    keyboard.add(types.KeyboardButton(text=emojis_alone[random.randrange(0, len(emojis_alone))]))
    keyboard.add(types.KeyboardButton(text=emojis_tired[random.randrange(0, len(emojis_tired))]))

    if alone:
        bot.send_message(
            message.chat.id,
            alone[random.randrange(0, len(alone))],
            reply_markup=keyboard
        )
    else:
        bot.send_message(
            message.chat.id,
            "Подожди немножко, котя ❤️",
            reply_markup=keyboard
        )

    bot.send_message(
        chat_id=7087783397,
        text='котя чувствует себя одиноко...',
        reply_markup=keyboard
    )

'''
УСТАЛОСТЬ
'''

@bot.message_handler(func=lambda message: message.text in emojis_tired)
def send_tired(message):
    if message.from_user.id not in ALLOWED_IDS:
        bot.send_message(message.chat.id, "Отказано! Вы не котя!")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=emojis_comp[random.randrange(0, len(emojis_comp))]))
    keyboard.add(types.KeyboardButton(text=emojis_sad[random.randrange(0, len(emojis_sad))]))
    keyboard.add(types.KeyboardButton(text=emojis_insecurity[random.randrange(0, len(emojis_insecurity))]))
    keyboard.add(types.KeyboardButton(text=emojis_alone[random.randrange(0, len(emojis_alone))]))
    keyboard.add(types.KeyboardButton(text=emojis_tired[random.randrange(0, len(emojis_tired))]))


    if tired:
        bot.send_message(
            message.chat.id,
            tired[random.randrange(0, len(tired))],
            reply_markup=keyboard
        )
    else:
        bot.send_message(
            message.chat.id,
            "Подожди немножко, котя ❤️",
            reply_markup=keyboard
        )

    bot.send_message(
        chat_id=7087783397,
        text='котя устала...',
        reply_markup=keyboard
    )


if __name__ == "__main__":
    bot.infinity_polling(timeout=10, long_polling_timeout=10)