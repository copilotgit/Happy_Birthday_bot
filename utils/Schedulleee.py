from utils.Database import Database
from datetime import datetime
from pytz import timezone
db = Database()

async def check_birthdays(bot):
    birthdays = db.get_all()
    today = str(datetime.now(timezone("Etc/GMT+5")).strftime("%d-%m"))
    yil = int(datetime.now().strftime("%Y"))
    print(today)
    for i in birthdays:
        if i[6][:5] == today:
            await bot.send_photo(chat_id=int(((i[7]).split(":"))[1]), photo=i[5], caption=f"#happy_birthday\nAssalomu alaykum, hammaga. Bugun <b>{i[2]} {i[3]} {i[4]}</b>ning tug'ilgan kunlari🎉🥳. {yil-int((i[6])[6:])} yoshingiz muborak bo'lsin🥰. Boshimizga doim sog' bo'ling, bunaqa tug'ilgan kunlardan ko'pini ko'ring. Tug'ilgan kuningizni yaxshi o'tkazing 🎊🎉")