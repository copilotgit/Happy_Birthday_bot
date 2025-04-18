from aiogram import Router
from aiogram.types import Message

dp = Router()

@dp.message()
async def echo(message: Message):
    # await message.send_copy(message.from_user.id)
    pass
