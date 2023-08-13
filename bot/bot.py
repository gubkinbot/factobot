import os
from dotenv import load_dotenv
import telebot
from telebot import types
import random
import string
import openai
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine


load_dotenv('../.env')

bot_token = os.environ.get('TG_FACTOBOT')
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

DB_FACT_HOST = os.getenv("DB_FACT_HOST")
DB_FACT_USER = os.getenv("DB_FACT_USER")
DB_FACT_PASSWORD = os.getenv("DB_FACT_PASSWORD")
DB_FACT_NAME = os.getenv("DB_FACT_NAME")

engine = create_engine(f"mysql+mysqlconnector://{DB_FACT_USER}:{DB_FACT_PASSWORD}@{DB_FACT_HOST}/{DB_FACT_NAME}")

bot = telebot.TeleBot(bot_token)

def generate_password():
    return ''.join(random.choice(string.digits) for _ in range(5))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    password = generate_password()
    response = f'''<b>Добро пожаловать в @factobot!</b>

Здесь собраны все короткие заметки студентов IT-академии Uzum по направлению анализ данных и машинное обучение.

Заносите свои заметки через factobot.uz, используя ваши личные учетные данные:
Логин: <pre>{message.chat.id}</pre>
Пароль: <pre>{password}</pre>

🗒 Просматривайте свои и чужие заметки, используя команду /fact.

🤖 Если что-то не понятно — спрашивайте, вам ответит ChatGPT.

⚖️ Оценивайте заметки. Хорошие заметки будут показываться чаще, плохие — реже.
'''
    bot.send_message(message.chat.id, response, parse_mode='HTML')

@bot.message_handler(commands=['fact'])
def send_fact(message):
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                        messages=[
                                            {"role": "system", "content": "You are an experienced Data Science Specialist. Students come to you. They need short useful practical notes. The length of the note should not exceed two sentences. The note should be on any one of the following topics: Python programming, basic machine learning algorithms, Python libraries: pandas, sklearn, numpy, plotly, seaborn. You need to answer only in Russian."},
                                            {"role": "user", "content": "give practical note"}])
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('👍', callback_data='good')
    item2 = types.InlineKeyboardButton('👎', callback_data='bad')
    markup.add(item1, item2)
    fact = pd.read_sql_query(sql='SELECT * FROM facts ORDER BY RAND() LIMIT 1;', con=engine)
    formatted_text = f'''<strong>{fact.iloc[0].note_id}</strong>

{fact.iloc[0].note_text}
'''
    bot.send_message(chat_id=message.chat.id, text=formatted_text, reply_markup=markup, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(chat_id=message.chat.id, text='Ответ ChatGPT', parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'bad':
        bot.answer_callback_query(call.id, "Большое этого не будет")
    elif call.data == 'good':
        bot.answer_callback_query(call.id, "Агонь, согласен!")

bot.polling()