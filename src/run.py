import logging
from aiogram import Bot, Dispatcher, executor, types
import registration
import facts
import yaml
from os import path as os_path

config_path = os_path.abspath(os_path.join(os_path.dirname(__file__), 'config.yml'))
config = yaml.safe_load(open(config_path))

fact_button = types.InlineKeyboardButton('Ещё!', callback_data='next')
inline_fact_button = types.InlineKeyboardMarkup().add(fact_button)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config['TOKEN'])
dp = Dispatcher(bot)



@dp.callback_query_handler(text='next')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    await query.answer("Let's Rock!")
    await query.message.edit_text(text=facts.get_fact(), reply_markup=inline_fact_button, parse_mode='html')
#     await bot.send_message(query.from_user.id, facts.get_fact(), parse_mode='html', reply_markup=inline_fact_button)
#     await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="тру-ту-ту", reply_markup=key )

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(registration.start(message.chat.id), parse_mode='html')
    
@dp.message_handler(commands=['fact'])
async def send_welcome(message: types.Message):
    await message.reply(facts.get_fact(), parse_mode='html', reply_markup=inline_fact_button)
    
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
