from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import db_session
from middlewares import AccessMiddleware
from settings import settings

bot = Bot(token=settings.bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(AccessMiddleware(settings.allowed_user_ids))

settings.database_path.parent.mkdir(parents=True, exist_ok=True)
db_session.global_init(str(settings.database_path))
