import random
import mysql.connector
import yaml
from os import path as os_path

config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
data = yaml.safe_load(open(config_path))

def start(user_id):
    mydb = mysql.connector.connect(
        host=data['DB_HOST'],
        user=data['DB_USERNAME'],
        password=data['DB_PASSWORD'],
        database=data['DB_NAME'])
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    myresult = mycursor.rowcount
    myresult_data = mycursor.fetchone()
    
    if myresult >= 1:
        mycursor.close()
        mydb.close()
        return f'''Вы уже авторизованы в системе.'''
    
    new_login = get_login()
    new_password = get_password()
    mycursor = mydb.cursor(buffered=True)
    sql = "INSERT INTO users (user_id, username, password) VALUES (%s, %s, %s)"
    val = (user_id, new_login, new_password)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "record inserted.")
    
    return f'''<b>Добро пожаловать!</b>
    
Вы находитесь в боте для принятия ответов на вопросы IV игры Чемпионата "Что? Где? Когда?" среди организаций Группы "ЛУКОЙЛ".
Для продолжения, пожалуйста, авторизуйтесь, отправив свой номер телефона, либо нажмите на кнопку в нижней части экрана.
Поддержка — @samorukov'''
