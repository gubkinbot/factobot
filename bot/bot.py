import os
from dotenv import load_dotenv
import telebot
from telebot import types

load_dotenv('./.env')

bot_token = os.environ.get('TG_FACTOBOT')

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    response = "Hello! I am your simple Telegram bot. Send me a message, and I'll echo it back."
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('Кнопка 1')
    item2 = types.KeyboardButton('Кнопка 2')
    markup.add(item1, item2)
    bot.reply_to(message, f'кукареку: {message.text}', reply_markup=markup)

bot.polling()