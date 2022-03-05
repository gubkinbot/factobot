import random
import mysql.connector
import yaml
from os import path as os_path

config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
data = yaml.safe_load(open(config_path))

def get_fact(old_fact):
  new_fact = extract_fact()
  return '>>' + new_fact + '<<' + '>>' + old_fact + '<<'

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
  
  note = myresult[2]
  code = myresult[3]
  message = f'<i>{note}</i>\n\n<code>{code}</code>'
  return message
