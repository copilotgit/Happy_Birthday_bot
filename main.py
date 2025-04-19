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
# from aiogram.types import Update
# from aiohttp import web

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


#____________________________________________________________________________#
# async def on_startup(app):
#     await bot.set_webhook('https://nasrullonutfullayev.pythonanywhere.com/')

# async def on_shutdown(app):
#     await bot.delete_webhook()

# async def handle_update(request):
#     request_json = await request.json()
#     update = Update.to_object(request_json)
#     await dp._process_update(update)
#     return web.Response()

# app = web.Application()
# app.router.add_post('/', handle_update)
# app.on_startup.append(on_startup)
# app.on_shutdown.append(on_shutdown)
# app.on_shutdown.append(start_scheduler)

# if __name__ == '__main__':
#     web.run_app(app, port=8000)
# #____________________________________________________________________________#
