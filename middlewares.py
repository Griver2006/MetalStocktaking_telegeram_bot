from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AccessMiddleware(BaseMiddleware):
    def __init__(self, allowed_user_ids):
        super().__init__()
        self.allowed_user_ids = allowed_user_ids

    async def on_pre_process_message(self, message: types.Message, data: dict):
        if message.from_user.id not in self.allowed_user_ids:
            await message.answer("Доступ запрещён.")
            raise CancelHandler()

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        if query.from_user.id not in self.allowed_user_ids:
            await query.answer("Доступ запрещён.", show_alert=True)
            raise CancelHandler()
