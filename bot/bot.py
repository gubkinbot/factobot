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
    check_user = pd.read_sql_query(sql=f'SELECT * FROM `users` WHERE username = {message.chat.id}', con=engine)
    if len(check_user) > 0:
        password = check_user.iloc[0].password
        pd.DataFrame(columns=['user_id', 'action'], data=[[message.chat.id, '/start']]).to_sql(name='log', con=engine, if_exists='append', index=False)
    else:
        password = generate_password()
        pd.DataFrame(columns=['username', 'password'], data=[[message.chat.id, password]]).to_sql(name='users', con=engine, if_exists='append', index=False)
        pd.DataFrame(columns=['user_id', 'action'], data=[[message.chat.id, 'reg']]).to_sql(name='log', con=engine, if_exists='append', index=False)
    response = f'''<b>Добро пожаловать в @factobot!</b>

Здесь собраны все короткие заметки студентов IT-академии Uzum по направлениям анализа данных и машинного обучения.

Заносите свои заметки через factobot.uz, используя личные учетные данные:
Логин: <pre>{message.chat.id}</pre>
Пароль: <pre>{password}</pre>

🗒 Просматривайте свои и чужие заметки, используя команду /fact.

🤖 Если что-то не понятно — спрашивайте, вам ответит ChatGPT.

⚖️ Оценивайте заметки. Хорошие заметки будут показываться чаще, плохие — реже.
''' 	 	
    bot.send_message(message.chat.id, response, parse_mode='HTML')

@bot.message_handler(commands=['settings'])
def send_welcome(message):
    pd.DataFrame(columns=['user_id', 'action'], data=[[message.chat.id, '/settings']]).to_sql(name='log', con=engine, if_exists='append', index=False)
    bot.send_message(message.chat.id, 'В разработке. Здесь будет статистика использования, возможность отключения общего пула заметок.', parse_mode='HTML')

@bot.message_handler(commands=['fact'])
def send_fact(message):
    fact = pd.read_sql_query(sql='SELECT * FROM facts ORDER BY RAND() LIMIT 1;', con=engine)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('👍', callback_data=f'good|{fact.iloc[0].note_id}')
    item2 = types.InlineKeyboardButton('👎', callback_data=f'bad|{fact.iloc[0].note_id}')
    markup.add(item1, item2)
    formatted_text = f'''<strong>{fact.iloc[0].note_id}</strong>

{fact.iloc[0].note_text}'''	 
    pd.DataFrame(columns=['user_id', 'action', 'note_id'], data=[[message.chat.id, 'fact', fact.iloc[0].note_id]]).to_sql(name='log', con=engine, if_exists='append', index=False)
    bot.send_message(chat_id=message.chat.id, text=formatted_text, reply_markup=markup, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    history = pd.read_sql_query(sql=f"SELECT * FROM `log` WHERE user_id = {message.chat.id} order by datetime desc limit 10", con=engine)
    if history.iloc[0].action == '/fact':
        bot.send_message(chat_id=message.chat.id, text='можно отвечать, последняя запись по факту', parse_mode='HTML')
        response = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                        messages=[
                                            {"role": "system", "content": "You are an experienced Data Science Specialist. Students come to you. They need short useful practical notes. The length of the note should not exceed two sentences. The note should be on any one of the following topics: Python programming, basic machine learning algorithms, Python libraries: pandas, sklearn, numpy, plotly, seaborn. You need to answer only in Russian."},
                                            {"role": "user", "content": message.text}])
        bot.send_message(chat_id=message.chat.id, text=response['choices'][0]['message']['content'], parse_mode='HTML')
    else:
        bot.send_message(chat_id=message.chat.id, text='Пожалуйста, ознакомьтесь с заметкой с помощью команды /fact, а затем задавайте вопросы', parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    call_data_array = call.data.split('|')
    if call_data_array[0] == 'bad':
        pd.DataFrame(columns=['user_id', 'note_id', 'rating'], data=[[call.from_user.id, call_data_array[1], 'bad']]).to_sql(name='ratings', con=engine, if_exists='append', index=False)
        bot.answer_callback_query(call.id, f"Безобразие!{call_data_array[1]}")
    elif call_data_array[0] == 'good':
        pd.DataFrame(columns=['user_id', 'note_id', 'rating'], data=[[call.from_user.id, call_data_array[1], 'good']]).to_sql(name='ratings', con=engine, if_exists='append', index=False)
        bot.answer_callback_query(call.id, f"Агонь, согласен!{call_data_array[1]}")

bot.polling()