import random
import mysql.connector
import yaml
from os import path as os_path

config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
data = yaml.safe_load(open(config_path))

def start(user_id):
    mydb = mysql.connector.connect(
        host=data['CHGK_DB_HOST'],
        user=data['CHGK_DB_USERNAME'],
        password=data['CHGK_DB_PASSWORD'],
        database=data['CHGK_DB_NAME'])
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM 'TABLE 1' WHERE user_id = '{user_id}'")
    myresult = mycursor.rowcount
    myresult_data = mycursor.fetchone()
    
    if myresult >= 1:
        mycursor.close()
        mydb.close()
        return f'''Вы уже авторизованы в системе.'''
    
    mydb.close()
    
    return f'''<b>Добро пожаловать!</b>
    
Вы находитесь в боте для принятия ответов на вопросы IV игры Чемпионата "Что? Где? Когда?" среди организаций Группы "ЛУКОЙЛ".
Для продолжения, пожалуйста, авторизуйтесь, отправив свой номер телефона, либо нажмите на кнопку в нижней части экрана.
Поддержка — @samorukov'''
