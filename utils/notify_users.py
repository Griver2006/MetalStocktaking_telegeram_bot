from utils.some_variable import metal_types

from keyboards.reply_kb_menu import reply_kb_menu

from data import db_session
from data.users import User


async def for_startup(dp):
    # При запуске бота возвращяем всех пользователей в меню
    dbs = db_session.create_session()
    for user in dbs.query(User).all():
        user.metal = 'Черный'
        user.price = float(metal_types['Черный'])
        user.client_amount = 0
        user.kush_recording = False
        user.operation_ended = False
        user.kush_percent = 0
        await dp.bot.send_message(user.id, 'Бот запущен!', reply_markup=reply_kb_menu)
    dbs.commit()
