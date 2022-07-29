from aiogram import executor, types
from aiogram.utils.executor import start_webhook

from loader import dp, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
import handlers
from utils.notify_users import for_startup
import utils.set_default_commands


async def on_startup(dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("update_prices", "Обновить цены")])
    await dp.bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    await for_startup(dispatcher)


async def on_shutdown(dispatcher):
    await dp.bot.delete_webhook()


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )