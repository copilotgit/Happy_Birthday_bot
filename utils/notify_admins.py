from data.config import ADMINS

async def on_startup_notify(bot):
    for admin in ADMINS:
        try:
            await bot.send_message(admin, "Bot ishga tushdi ✅")
        except:
            print(f"{admin} ga xabar yuborib bo'lmadi")
