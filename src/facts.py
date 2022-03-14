import random
import mysql.connector
import yaml
from os import path as os_path

config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
data = yaml.safe_load(open(config_path))

def extract_fact(user_id):  
  mydb = mysql.connector.connect(
  host=data['DB_HOST'],
  user=data['DB_USERNAME'],
  password=data['DB_PASSWORD'],
  database=data['DB_NAME'])

  mycursor = mydb.cursor(buffered=True)
  mycursor.execute(f"SELECT * FROM facts WHERE user_id = {user_id} ORDER BY RAND() LIMIT 1 ")
  myresult = mycursor.fetchone()
  mycursor.close()
  mydb.close()
#   title = myresult[5]
#   link = myresult[6]
#   note = myresult[2]
#   code = myresult[3]
  
  title, link, note, code = '', '', '', ''
  if len(myresult[5]) > 0:
    title = f'<b>{myresult[5]}</b>\n\n'
  if len(myresult[6]) > 0:
    link = f'<a href="{myresult[6]}">Источник</a>'
  if len(myresult[2]) > 0:
    note = f'<i>{myresult[2]}</i>\n\n'
  if len(myresult[3]) > 0:
    code = f'<pre><code class="language-python">{myresult[3]}</code></pre>\n\n'
  message = f'{title}{code}{note}{link}'
#   message = f'<b>{title}</b>\n\n<pre><code class="language-python">{code}</code></pre>\n\n<i>{note}</i>\n\n<a href="{link}">Источник</a>'
  return message
