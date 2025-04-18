from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Any, Dict

class MessageLoggerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        print(f"🆔: {event.from_user.id}, 👤Full name: {event.from_user.full_name}, Username: @{event.from_user.username}\n📝Text: {event.text}")
        return await handler(event, data)
