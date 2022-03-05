import logging
from aiogram import Bot, Dispatcher, executor, types
import registration
import facts
import yaml
from os import path as os_path
import aiomysql

config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
config = yaml.safe_load(open(config_path))


next_button = types.InlineKeyboardButton('Ещё!', callback_data='next')
inline_fact_button = types.InlineKeyboardMarkup().row(next_button)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config['TOKEN'])
dp = Dispatcher(bot)



@dp.callback_query_handler(text='next')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    await query.answer()
    await query.message.edit_text(text=f'csdcsdcsacdsdcasdc', reply_markup=inline_fact_button, parse_mode='html')

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(registration.start(message.chat.id), parse_mode='html')
    
@dp.message_handler(commands=['fact'])
async def send_welcome(message: types.Message):
    mydb = await aiomysql.aiomysql.connect(host=data['DB_HOST'], user=data['DB_USERNAME'], password=data['DB_PASSWORD'], db=data['DB_NAME'])
    await message.reply('csdcsdcsdcsdc', parse_mode='html', reply_markup=inline_fact_button)
    
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
