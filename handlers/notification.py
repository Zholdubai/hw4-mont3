from aiogram import types, Dispatcher
from database import sql_command_all
from config import bot
import asyncio
import aioschedule
import random

async def reklama():
    result = await sql_command_all()
    r_u = random.randint(0, len(result) - 1)
    await bot.send_photo(chat_id=chat_id, photo=result[r_u][3],
                         caption=f'Name: {result[r_u][3]}\n'
                                 f'Photo: {result[r_u][2]}\n'
                                 f'Description: {result[r_u][4]}\n'
                                 f'Price: {result[r_u][5]}\n\n'
                                 f'{result[r_u][1]}')
print(reklama())
async def schedule():
    aioschedule.every().day.at('19:59').do(reklama)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def echo_message(message: types.Message):
    global chat_id
    chat_id = message.chat.id
#notification
    if message.text == 'reklama':
        await message.reply('ok')
        await schedule()

def register_hendlers_notification(dp: Dispatcher):
    dp.register_message_handler(echo_message)



