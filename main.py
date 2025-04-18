import asyncio
import logging
from aiogram import Bot, Dispatcher
from data.config import TOKEN
from handlers import routers
from middlewares.message_middleware import MessageLoggerMiddleware
from middlewares.callback_middleware import CallbackLoggerMiddleware
from utils.notify_admins import on_startup_notify
from utils.set_bot_cmmands import set_bot_commands
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.Schedulleee import check_birthdays

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.message.middleware(MessageLoggerMiddleware())
dp.callback_query.middleware(CallbackLoggerMiddleware())

scheduler = AsyncIOScheduler()

async def start_scheduler(bot):
    scheduler.add_job(check_birthdays, "cron", hour=16, minute=4, args=[bot])
    scheduler.start()
    await asyncio.Event().wait()  # Keeps the event loop running


async def main():
    for router in routers:
        dp.include_router(router)
    await set_bot_commands(bot)
    await on_startup_notify(bot)
    await asyncio.gather(
    dp.start_polling(bot),
    start_scheduler(bot),
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
