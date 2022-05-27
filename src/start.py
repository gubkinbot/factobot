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
    mycursor.execute(f"SELECT * FROM `TABLE 1` WHERE `user_id` = {int(user_id)}")
    myresult = mycursor.rowcount
    myresult_data = mycursor.fetchone()
    
    if myresult >= 1:
        mycursor.close()
        mydb.close()
        return f'''Вы уже авторизованы! Игра начнётся в 13:00 по московскому времени.'''
    
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "record inserted.")
    
    return f'''<b>Добро пожаловать!</b>

Для продолжения, пожалуйста, отправьте свой номер телефона или нажмите на кнопку в нижней части экрана
'''
