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
        return f'''@factobot поможет держать в памяти важную информацию из области Data Science и Python!
Используй команду /fact для получения заметок, /settings для управления рассылкой.
Ты также можешь добавить собственные заметки через форму на сайте factobot.tech, используя личные учетные данные:
Идентификатор: <pre>{myresult_data[2]}</pre>
Пароль: <pre>{myresult_data[3]}</pre>
Подробнее — factobot.tech/about
Поддержка — @samorukov'''
    
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "record inserted.")
    
    return f'''<b>Добро пожаловать!</b>
    
'''
