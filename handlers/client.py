from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types, Dispatcher
from config import bot, dp, ADMIN
from database import bot_db

async def show_random_user(message:types.Message):
    await bot_db.sql_command_random(message)

def register_hendlers_client(dp:Dispatcher):
    dp.register_message_handler(show_random_user, commands=['random'])
