import random
import mysql.connector
import yaml
from os import path as os_path

config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
data = yaml.safe_load(open(config_path))

def get_fact():
  mydb = mysql.connector.connect(
    host=data['DB_HOST'],
    user=data['DB_USERNAME'],
    password=data['DB_PASSWORD'],
    database=data['DB_NAME'])
  mycursor = mydb.cursor(buffered=True)
  mycursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
  myresult = mycursor.fetchone()
  mycursor.close()
  mydb.close()
  return str(myresult)
