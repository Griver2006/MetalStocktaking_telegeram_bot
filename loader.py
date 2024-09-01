from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

from data import db_session

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    print('Введите токен вашего бота в .env!')
    exit()

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db_session.global_init("db/Metals_with_data.db")