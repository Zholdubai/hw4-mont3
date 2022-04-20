from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMIN
from database import bot_db
from .keyboards import cancel_markup

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
#start
async def fsm_start(message:types.Message):
    if message.chat.type == 'private':
      await FSMAdmin.photo.set()
      await bot.send_message(message.chat.id, f'Privet {message.from_user.full_name} skin fotku',
                             reply_markup=cancel_markup)
    else:
        await message.answer('V lichku pishi')
#foto

async def photo_bludo(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['nickname'] = f"@{message.from_user.username}"
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, "Kak nazivaetsia bludo?")


#  name
async def bludo_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, "Opisanie kak?")


# description
async def description_bludo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['opisanie'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, "skolko stoit (tolko so siframi?")

#price
async def bludo_price(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['price'] = int(message.text)
        await bot_db.sql_command_insert(state)
        await state.finish()
        await bot.send_message(message.chat.id, "Spasibo za interes")
    except:
        await bot.send_message(message.chat.id, "Ja skazal tolko chislami!!!")


async def cancal_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply("ОК")
async def delete_data(message:types.Message):
    if message.from_user.id == ADMIN:
        results = await bot_db.sql_command_all(message)
        for result in results:
            await bot.send_photo(message.from_user.id, result[2],
                                 caption=f'Name: {result[3]}\n'
                                         f'Photo: {result[2]}\n'
                                         f'Description: {result[4]}\n'
                                         f'Price: {result[5]}\n\n'
                                         f'{result[1]}',
                                 reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                 f'delete:{result[3]}',
                                 callback_data=f'delete:{result[0]}')))
    else:
        await message.answer('Ti ne admin')
async def complete_delete(call:types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace('delet:', ''))
    await call.answer(text=f"{call.data.replace('delet:', '')} deleted", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_hendler_fsmAdminGetUser(dp: Dispatcher):
    dp.register_message_handler(cancal_reg, state="*", commands="cancel")
    dp.register_message_handler(cancal_reg, Text(equals='cancel', ignore_case=True), state="*")

    dp.register_message_handler(fsm_start, commands=["menu"])
    dp.register_message_handler(photo_bludo, state=FSMAdmin.photo, content_types=["photo"])
    dp.register_message_handler(bludo_name, state=FSMAdmin.name)
    dp.register_message_handler(description_bludo, state=FSMAdmin.description)
    dp.register_message_handler(bludo_price, state=FSMAdmin.price)

    dp.register_message_handler(delete_data, commands=['delete'])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call:call.data and call.data.startwith('delete:'))




