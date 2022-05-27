
import yaml
from os import path as os_path
import telebot
import facts
import registration
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# test

config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
config = yaml.safe_load(open(config_path))

bot = telebot.TeleBot(config['TOKEN'])

fact_markup = InlineKeyboardMarkup()
fact_markup.add(InlineKeyboardButton('Ещё!', callback_data="next"))

settings_markup = InlineKeyboardMarkup(row_width=1)
settings_markup.add(InlineKeyboardButton('Приватность', callback_data="privacy"), InlineKeyboardButton('Рассылка', callback_data="alarm"))

@bot.message_handler(commands=['start', 'info'])
def send_welcome(message):
    bot.reply_to(message, registration.start(message.chat.id), parse_mode='html')

@bot.message_handler(commands='settings')
def send_welcome(message):
    bot.reply_to(message, 'Управление приватностью и рассылкой:',
                 reply_markup=settings_markup, parse_mode='html')

@bot.message_handler(commands='fact')
def send_welcome(message):
    bot.send_message(message.chat.id, facts.extract_fact(message.chat.id), reply_markup=fact_markup, parse_mode='html', disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'next':
        bot.answer_callback_query(call.id, "Едем дальше...")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=facts.extract_fact(call.message.chat.id), reply_markup=fact_markup, disable_web_page_preview=True, parse_mode='html')
    elif call.data == 'privacy':
        bot.answer_callback_query(call.id, "Приватность в разработке")
    elif call.data == 'alarm':
        bot.answer_callback_query(call.id, "Рассылка в разработке")
        
bot.infinity_polling()
