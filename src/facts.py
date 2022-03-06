import random
import mysql.connector
import yaml
from os import path as os_path

config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
data = yaml.safe_load(open(config_path))

def extract_fact():  
  mydb = mysql.connector.connect(
  host=data['DB_HOST'],
  user=data['DB_USERNAME'],
  password=data['DB_PASSWORD'],
  database=data['DB_NAME'])

  mycursor = mydb.cursor(buffered=True)
  mycursor.execute("SELECT * FROM facts ORDER BY RAND() LIMIT 1")
  myresult = mycursor.fetchone()
  mycursor.close()
  mydb.close()
  title = myresult[5]
  link = myresult[6]
  note = myresult[2]
  code = myresult[3]
  message = f'<b>{title}</b>\n\n<pre language="python">{code}</pre>\n\n<i>{note}</i>\n\n<a href="{link}">inline URL</a>'
  return message
