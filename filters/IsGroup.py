from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsGroup(BaseFilter):
    def __init__(self, F, bot_username):
        self.F = F
        self.username = bot_username

    async def __call__(self, message: Message) -> bool:
        return (message.chat.type in ["group", "supergroup"]) and (self.F.reply_to_message | self.F.text.contains(self.username))
    
class IsPrivate(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return (message.chat.type == "private")
    
