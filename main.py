from aiogram import executor
from config import dp
import logging
from handlers import callback, client, fsmAdminMenu, notification
from database import bot_db

async def on_startup(_):
    bot_db.sql_create()



fsmAdminMenu.register_hendler_fsmAdminGetUser(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)