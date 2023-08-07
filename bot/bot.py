import os
from dotenv import load_dotenv
import telebot

load_dotenv('./.env')

bot_token = os.environ.get('TG_FACTOBOT')

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    response = "Hello! I am your simple Telegram bot. Send me a message, and I'll echo it back."
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, f'кукареку: {message.text}')


bot.polling()