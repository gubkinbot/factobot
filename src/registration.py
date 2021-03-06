import random
import mysql.connector
import yaml
from os import path as os_path

config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
data = yaml.safe_load(open(config_path))

consonants = ['q', 'w', 'r', 't', 'p', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
vowels = ['a', 'e', 'y', 'u', 'i', 'o']
elements = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def get_login():
    return (random.choice(consonants) + 
            random.choice(vowels) + 
            random.choice(consonants) + 
            random.choice(vowels) + 
            random.choice(consonants) + 
            random.choice(vowels) + 
            random.choice(consonants))

def get_password():
    return ''.join([random.choice(elements) for i in range(8)])

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
        return f'''@factobot поможет держать в памяти важную информацию из области Data Science и Python!

Используй команду /fact для получения заметок, /settings для управления рассылкой.

Ты также можешь добавить собственные заметки через форму на сайте factobot.tech, используя личные учетные данные:
Идентификатор: <pre>{myresult_data[2]}</pre>
Пароль: <pre>{myresult_data[3]}</pre>

Подробнее — factobot.tech/about
Поддержка — @samorukov'''
    
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
    
@factobot поможет держать в памяти важную информацию из области Data Science и Python!

Используй команду /fact для получения заметок, /settings для управления рассылкой.

Ты также можешь добавить собственные заметки через форму на сайте factobot.tech, используя личные учетные данные:
Идентификатор: <pre>{new_login}</pre>
Пароль: <pre>{new_password}</pre>

Подробнее — factobot.tech/about
Поддержка — @samorukov'''
