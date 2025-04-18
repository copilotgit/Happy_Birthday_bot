from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router


dp = Router()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Assalomu alaykum, It's my birthday bot ga xush kelibsiz")
