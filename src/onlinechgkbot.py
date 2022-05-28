import yaml
from os import path as os_path
import telebot
import facts
import start
import mysql.connector
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import yaml
from os import path as os_path



config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
data = yaml.safe_load(open(config_path))


bot = telebot.TeleBot(data['ONLINECHGKBOT'])

fact_markup = InlineKeyboardMarkup()
fact_markup.add(InlineKeyboardButton('Ещё!', callback_data="next"))

settings_markup = InlineKeyboardMarkup(row_width=1)
settings_markup.add(InlineKeyboardButton('Приватность', callback_data="privacy"), InlineKeyboardButton('Рассылка', callback_data="alarm"))


@bot.message_handler(commands=['start', 'info'])
def send_welcome(message):
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text="Поделиться \ Share", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, f'''<b>Добро пожаловать!</b>
    
Для продолжения, пожалуйста, поделитесь своим номером телефона, нажав на кнопку в нижней части экрана

<b>Welcome!</b>
    
To continue, please share your phone number by clicking on the button at the bottom of the screen
''', reply_markup=keyboard, parse_mode='html')


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact.user_id == message.chat.id:
        mydb = mysql.connector.connect(
            host=data['DB_HOST'],
            user=data['DB_USERNAME'],
            password=data['DB_PASSWORD'],
            database=data['DB_NAME'])
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(f"SELECT * FROM `TABLE 1` WHERE `phone` = {str(message.contact.phone_number)[-11:]}")
        myresult = mycursor.rowcount
        myresult_data = mycursor.fetchone()
    
        if myresult >= 1:
            mycursor.close()
            mydb.close()
            mydb = mysql.connector.connect(
                host=data['DB_HOST'],
                user=data['DB_USERNAME'],
                password=data['DB_PASSWORD'],
                database=data['DB_NAME'])
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute(f"UPDATE `TABLE 1` SET `user_id`= {message.chat.id} WHERE phone = {str(message.contact.phone_number)[-11:]}")
            mydb.commit()
            mycursor.close()
            mydb.close()
            bot.send_message(message.chat.id, '''Авторизация прошла успешно. До встречи на игре!

Authorization was successful. See you at the game!''', reply_markup=ReplyKeyboardRemove())
        else:
            mycursor.close()
            mydb.close()
            bot.send_message(message.chat.id, '''Вашего номера нет в базе данных. Пожалуйста, обратитесь к @samorukov

Your number is not in the database. Please contact @samorukov''')
    else:
        bot.send_message(message.chat.id, '''Пожалуйста, отправьте свой номер телефона, который привязан к аккаунту Telegram

Please send your phone number which is linked to your Telegram account''')

        
@bot.message_handler(content_types=["text"])
def handle_text(message):
    
    mydb = mysql.connector.connect(
        host=data['DB_HOST'],
        user=data['DB_USERNAME'],
        password=data['DB_PASSWORD'],
        database=data['DB_NAME'])
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM `TABLE 1` WHERE `user_id` = {message.chat.id}")
    myresult = mycursor.rowcount
    myresult_data = mycursor.fetchone()
    if myresult >= 1:
        
        bot.send_message(message.chat.id, str(myresult_data))
    
        state = myresult_data[6]
        number = myresult_data[0]
        adr = "A_" + str(number)
        admin_id = myresult_data[7]
        bot.send_message(message.chat.id, f'state: {state}, number: {number}, admin_id: {admin_id}')
        if int(state) > 0:
            bot.send_message(message.chat.id, f'''вошли''')
            mycursor.close()
            mydb.close()
            bot.send_message(message.chat.id, f'''вошли 2''')
            mydb = mysql.connector.connect(
                host=data['DB_HOST'],
                user=data['DB_USERNAME'],
                password=data['DB_PASSWORD'],
                database=data['DB_NAME'])
            mycursor = mydb.cursor(buffered=True)
            bot.send_message(message.chat.id, f'''вошли 3''')
            mycursor.execute(f"UPDATE `TABLE 1` SET {adr} = `фвуфувыв`, state = 0 WHERE nn = {number}")
            mydb.commit()
            mycursor.close()
            mydb.close()
            bot.send_message(message.chat.id, f'''Ответ отправлен''')
        if int(state) == 0:
            bot.send_message(message.chat.id, f'''В данный момент ответы не принимаются.''')
    else:
        bot.send_message(message.chat.id, 'Наобходимо пройти авторизацию!')
    mycursor.close()
    mydb.close()

        
bot.infinity_polling()
