from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

from data import db_session

TOKEN = '5171093905:AAFRlbv5jY6TdQfqOtL03c8VCgtYzQfDwPg'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db_session.global_init("db/Metals_with_data.db")