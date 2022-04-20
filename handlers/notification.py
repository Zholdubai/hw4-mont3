from aiogram import types, Dispatcher
from config import bot, dp

async def echo_message(message: types.Message):
    def register_hendlers_notification(dp: Dispatcher):
        dp.register_message_handler(echo_message)

