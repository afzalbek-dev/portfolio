import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from bot.db import is_authorized_admin

logger = logging.getLogger(__name__)

class GlobalAdminAuthMiddleware(BaseMiddleware):
    """
    Global middleware that blocks all unauthorized users from accessing ANY command, message, callback, or FSM state.
    """
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user_id = None
        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery) and event.from_user:
            user_id = event.from_user.id

        if user_id and not is_authorized_admin(user_id):
            logger.warning(f"Unauthorized access attempt by Telegram ID: {user_id}")
            if isinstance(event, Message):
                await event.answer("⛔ **Access denied.** This is a private developer admin bot.", parse_mode="Markdown")
            elif isinstance(event, CallbackQuery):
                await event.answer("⛔ Access denied.", show_alert=True)
            return

        return await handler(event, data)
