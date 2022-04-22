import sqlite3
from config import bot
import random

def sql_create():
    global db, cursor
    db = sqlite3.connect('bot2.sqlite3')
    cursor = db.cursor()
    if db:
        print('Database is conneted!!!')
    db.execute('CREATE TABLE IF NOT EXISTS users'
               '(id INTEGER PRIMARY KEY, nickname TEXT, photo TEXT, name TEXT, description TEXT, price INTEGER)')
    db.commit()

async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values()))
        db.commit()

async def sql_command_random(message):
    result=cursor.execute('SELECT * FROM users').fetchall()
    r_u=random.randint(0, len(result)-1)
    await bot.send_photo(message.from_user.id, result[r_u][2],
                                       caption=f'Name: {result[r_u][3]}\n'
                                               f'Photo: {result[r_u][2]}\n'
                                               f'Description: {result[r_u][4]}\n'
                                               f'Price: {result[r_u][5]}\n\n'
                                               f'{result[r_u][1]}')
async def sql_command_all():
    return cursor.execute('SELECT * FROM users').fetchall()

async def sql_command_delete(id):
    cursor.execute('DELETE FROM users WHERE id == ?',(id))
    db.commit()
