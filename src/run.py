
import yaml
from os import path as os_path
import telebot
import facts
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
config = yaml.safe_load(open(config_path))

bot = telebot.TeleBot(config['TOKEN'])

markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton('Ещё!', callback_data="next"))

@bot.message_handler(commands=['start', 'info'])
def send_welcome(message):
    bot.reply_to(message, 'привет!')

@bot.message_handler(commands='settings')
def send_welcome(message):
    bot.reply_to(message, 'Настройки!')

@bot.message_handler(commands='fact')
def send_welcome(message):
    bot.send_message(message.chat.id, facts.extract_fact(), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "Едем дальше...")
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=facts.extract_fact(), reply_markup=markup)

bot.infinity_polling()
