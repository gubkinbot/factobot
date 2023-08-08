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
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('🤔', callback_data='what')
    item2 = types.InlineKeyboardButton('👍', callback_data='good')
    markup.add(item1, item2)
    formatted_text = f"Это текст, в котором есть скрытый текст: \n\n ||spoiler|| Скрытый текст:"
    bot.send_message(chat_id=message.chat.id, text=formatted_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'what':
        bot.answer_callback_query(call.id, "Вы что-то не поняли?")
    elif call.data == 'good':
        bot.answer_callback_query(call.id, "Агонь, да!")

bot.polling()