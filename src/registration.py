import random
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv('./.env')
FACT_DB_NAME = os.environ.get('FACT_DB_NAME')
FACT_DB_USER = os.environ.get('FACT_DB_USER')
FACT_DB_PASSWORD = os.environ.get('FACT_DB_PASSWORD')

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
  return f'''<b>Welcome!</b>

Your login: <pre>{get_login()}</pre>
Your password: <pre>{get_password()}</pre>
{FACT_DB_NAME}'''
