from aiogram import types
from api_sheets import call_metals_prices
from data import db_session
from data.clean_weights import ButtonsCleanWeights
from loader import dp
from keyboards.reply_kb_menu import reply_kb_menu


metal_types = dict(call_metals_prices())
kush_prices = dict(call_metals_prices(kush=True))
clean_weights_buttons = [name[0] for name in db_session.create_session().query(
    ButtonsCleanWeights.name_clean_weight).all()]

temp_operations = {}


@dp.message_handler(commands=['update_prices'])
async def update_prices(message: types.Message):
    global metal_types, kush_prices
    request_metals_types = call_metals_prices()
    if not request_metals_types:
        request_metals_types = call_metals_prices()
    request_kush_prices = call_metals_prices(kush=True)
    if not request_kush_prices:
        request_kush_prices = call_metals_prices(kush=True)
    metal_types = dict(request_metals_types)
    kush_prices = dict(request_kush_prices)
    await message.bot.send_message(message.chat.id, 'Цены обновлены!', reply_markup=reply_kb_menu)