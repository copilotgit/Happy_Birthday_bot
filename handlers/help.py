from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

dp = Router()

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Bu bot tug'ilgan kunlarni qo'shish va do'stlaringizni hamda oila a'zolaringizni tabriklovchi bot\n" \
    "/register - Tug'ilgan kuningizni qo'shish\n" \
    "/list_birthdays - Tug'ilgan kunlar ro'yxatini ko'rish\n" \
    "/my_birthdays - Men qo'shgan tug'ilgan kunlar ro'yxati(faqat shaxsiyda ishlaydi)")


