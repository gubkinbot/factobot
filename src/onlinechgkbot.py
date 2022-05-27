import yaml
from os import path as os_path
import telebot
import facts
import start
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
config = yaml.safe_load(open(config_path))

bot = telebot.TeleBot(config['ONLINECHGKBOT'])

fact_markup = InlineKeyboardMarkup()
fact_markup.add(InlineKeyboardButton('Ещё!', callback_data="next"))

settings_markup = InlineKeyboardMarkup(row_width=1)
settings_markup.add(InlineKeyboardButton('Приватность', callback_data="privacy"), InlineKeyboardButton('Рассылка', callback_data="alarm"))

@bot.message_handler(commands=['start', 'info'])
def send_welcome(message):
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) #Подключаем клавиатуру
    button_phone = KeyboardButton(text="Поделиться \ Share", request_contact=True) #Указываем название кнопки, которая появится у пользователя
    keyboard.add(button_phone) #Добавляем эту кнопку
    bot.send_message(message.chat.id, f'''<b>Добро пожаловать!</b>
    
Для продолжения, пожалуйста, поделитесь своим номером телефона, нажав на кнопку в нижней части экрана

<b>Welcome!</b>
    
To continue, please share your phone number by clicking on the button at the bottom of the screen
''', reply_markup=keyboard, parse_mode='html')
    
    
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


@bot.message_handler(content_types=['contact']) #Объявили ветку, в которой прописываем логику на тот случай, если пользователь решит прислать номер телефона :) 
def contact(message):
    if message.contact is not None: #Если присланный объект <strong>contact</strong> не равен нулю
        bot.send_message(message.chat.id, f'Понял, принял: {message.contact.phone_number}', reply_markup=ReplyKeyboardRemove())
        
bot.infinity_polling()
