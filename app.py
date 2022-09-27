from aiogram import executor, types
from aiogram.utils.executor import start_webhook

from loader import dp
import handlers
from utils.notify_users import for_startup
import utils.set_default_commands


async def on_startup(dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("update_prices", "Обновить цены")])
    await for_startup(dispatcher)


async def on_shutdown(dispatcher):
    await dp.bot.delete_webhook()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=for_startup)