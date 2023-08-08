import os
from dotenv import load_dotenv
import telebot
from telebot import types
import random
import string
# import openai

load_dotenv('./.env')

bot_token = os.environ.get('TG_FACTOBOT')
aaa = os.getenv("OPENAI_ORG")
uuu = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(bot_token)

def generate_password():
    return ''.join(random.choice(string.digits) for _ in range(5))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    password = generate_password()
    response = f'''Добро пожаловать в @factobot!

Заносите интересные факты, которые узнали в IT-академии Uzum через factobot.uz, используя ваши учетные данные:
Логин: <pre>{message.chat.id}</pre>
Пароль: <pre>{password}</pre>
'''
    bot.send_message(message.chat.id, response, parse_mode='HTML')

@bot.message_handler(commands=['fact'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('🤔', callback_data='what')
    item2 = types.InlineKeyboardButton('👍', callback_data='good')
    markup.add(item1, item2)
    formatted_text = f'''<strong>List Comprehension</strong>

<tg-spoiler>List comprehension offers a shorter syntax when you want to create a new list based on the values of an existing list.</tg-spoiler>

<tg-spoiler><code>&gt;&gt;&gt; [i for i in range(5)]</code></tg-spoiler>
<tg-spoiler><code>[0, 1, 2, 3, 4]</code></tg-spoiler>
{aaa}
{uuu}'''
    bot.send_message(chat_id=message.chat.id, text=formatted_text, reply_markup=markup, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('🤔', callback_data='what')
    item2 = types.InlineKeyboardButton('👍', callback_data='good')
    markup.add(item1, item2)
    formatted_text = f'''Это текст, в котором есть скрытый текст:

<tg-spoiler>spoiler spoiler spoiler spoiler spoiler spoiler spoiler spoiler spoiler spoiler spoiler spoiler spoiler spoiler </tg-spoiler>'''
    bot.send_message(chat_id=message.chat.id, text=formatted_text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'what':
        bot.answer_callback_query(call.id, "Вы что-то не поняли?")
    elif call.data == 'good':
        bot.answer_callback_query(call.id, "Агонь, да!")

bot.polling()