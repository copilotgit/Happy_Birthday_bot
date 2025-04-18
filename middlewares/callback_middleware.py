from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from typing import Callable, Awaitable, Dict, Any

class CallbackLoggerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        print(f"🆔: {event.from_user.id}, 👤Full name: {event.from_user.full_name}, Username: @{event.from_user.username}\n📝Text: {event.data}")
        return await handler(event, data)