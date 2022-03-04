import logging
from aiogram import Bot, Dispatcher, executor, types
import registration
import yaml
from os import path as os_path


config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
data = yaml.safe_load(open(config_path))
API_TOKEN = '118050171:AAGApBKKMUHXwOGJ2H7k0YZ715c75dPU0MQ'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(registration.start(message.chat.id), parse_mode='html')
    
@dp.message_handler(commands=['read'])
async def send_welcome(message: types.Message):
    await message.reply('Бот отправит запись из базы данных')
    
@dp.message_handler(commands=['write'])
async def send_welcome(message: types.Message):
    await message.reply('Можно будет добавить факт из бота')
    
@dp.message_handler(commands=['settings'])
async def send_welcome(message: types.Message):
    await message.reply('Настройки бота')

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f'"{message.text}" не является служебной командой. User_id: {message.chat.id}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
