import os
from dotenv import load_dotenv
import telebot
from telebot import types
import random
import string

load_dotenv('./.env')

bot_token = os.environ.get('TG_FACTOBOT')

bot = telebot.TeleBot(bot_token)

def generate_password():
    return ''.join(random.choice(string.digits) for _ in range(5))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    response = f'''Добро пожаловать в @factobot!

Заносите интересные факты, которые узнали в IT-академии Uzum через factobot.uz, используя ваши учетные данные:
Логин: `{message.chat.id}`
Пароль: `{generate_password()}`
'''
    bot.send_message(message.chat.id, response, parse_mode='MarkdownV2')

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('🤔', callback_data='what')
    item2 = types.InlineKeyboardButton('👍', callback_data='good')
    markup.add(item1, item2)
    formatted_text = f"Это текст, в котором есть скрытый текст: \n\n ||spoiler spoiler spoiler spoiler spoiler spoiler spoiler spoiler ||"
    bot.send_message(chat_id=message.chat.id, text=formatted_text, reply_markup=markup, parse_mode='MarkdownV2')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'what':
        bot.answer_callback_query(call.id, "Вы что-то не поняли?")
    elif call.data == 'good':
        bot.answer_callback_query(call.id, "Агонь, да!")

bot.polling()