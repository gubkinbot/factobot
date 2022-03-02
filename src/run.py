import logging
from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '118050171:AAGApBKKMUHXwOGJ2H7k0YZ715c75dPU0MQ'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Добро пожаловать в @factobot")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f'Вы отправили: {message.text}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
