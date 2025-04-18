from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

tasdiqlash = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "⬅️", callback_data="qaytib")],
    [InlineKeyboardButton(text = "❌", callback_data="yoq")],
    [InlineKeyboardButton(text = "✅", callback_data="ha")]
])

tasdiqlash_year = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "⬅️", callback_data="yqaytib")],
    [InlineKeyboardButton(text = "❌", callback_data="yyoq")],
    [InlineKeyboardButton(text = "✅", callback_data="yha")]
])


async def klaviatura(num = ""):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1️⃣", callback_data=f"num:{num}1"), InlineKeyboardButton(text="2️⃣", callback_data=f"num:{num}2"), InlineKeyboardButton(text="3️⃣", callback_data=f"num:{num}3")],
        [InlineKeyboardButton(text="4️⃣", callback_data=f"num:{num}4"), InlineKeyboardButton(text="5️⃣", callback_data=f"num:{num}5"), InlineKeyboardButton(text="6️⃣", callback_data=f"num:{num}6")],
        [InlineKeyboardButton(text="7️⃣", callback_data=f"num:{num}7"), InlineKeyboardButton(text="8️⃣", callback_data=f"num:{num}8"), InlineKeyboardButton(text="9️⃣", callback_data=f"num:{num}9")],
        [InlineKeyboardButton(text="❌", callback_data="bekor_qilish"), InlineKeyboardButton(text="0️⃣", callback_data=f"num:{num}0"), InlineKeyboardButton(text="⬅️", callback_data=f"num:none/{num}")]
    ])

klaviatura_oy = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Yanvar", callback_data="oy:01"), InlineKeyboardButton(text="Fevral", callback_data="oy:02"), InlineKeyboardButton(text="Mart", callback_data="oy:03")],
    [InlineKeyboardButton(text="Aprel", callback_data="oy:04"), InlineKeyboardButton(text="May", callback_data="oy:05"), InlineKeyboardButton(text="Iyun", callback_data="oy:06")],
    [InlineKeyboardButton(text="Iyul", callback_data="oy:07"), InlineKeyboardButton(text="Avgust", callback_data="oy:08"), InlineKeyboardButton(text="Sentyabr", callback_data="oy:09")],
    [InlineKeyboardButton(text="Oktyabr", callback_data="oy:10"), InlineKeyboardButton(text="Noyabr", callback_data="oy:11"), InlineKeyboardButton(text="Dekabr", callback_data="oy:12")],
    [InlineKeyboardButton(text="⬅️", callback_data="oy:100")]
])

# async def klaviatura_year(num = ""):
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="1️⃣", callback_data=f"num:{num}1"), InlineKeyboardButton(text="2️⃣", callback_data=f"num:{num}2"), InlineKeyboardButton(text="3️⃣", callback_data=f"num:{num}3")],
#         [InlineKeyboardButton(text="4️⃣", callback_data=f"num:{num}4"), InlineKeyboardButton(text="5️⃣", callback_data=f"num:{num}5"), InlineKeyboardButton(text="6️⃣", callback_data=f"num:{num}6")],
#         [InlineKeyboardButton(text="7️⃣", callback_data=f"num:{num}7"), InlineKeyboardButton(text="8️⃣", callback_data=f"num:{num}8"), InlineKeyboardButton(text="9️⃣", callback_data=f"num:{num}9")],
#         [InlineKeyboardButton(text=" ", callback_data="num:None"), InlineKeyboardButton(text="0️⃣", callback_data=f"num:{num}0"), InlineKeyboardButton(text="⬅️", callback_data=f"num:100/{num}")]
#     ])

async def bosing(link):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ro'yxatdan o'tish", url=link)]
    ])

async def paginate_birthdays(page):
    if page<0:
        return False
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️", callback_data=f"page:{page-1}"), InlineKeyboardButton(text="➡️", callback_data=f"page:{page+1}")]
    ])

async def paginate_my_birthdays(page, id_):
    if page<0:
        return False
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️", callback_data=f"bpage:{page-1}"), InlineKeyboardButton(text="➡️", callback_data=f"bpage:{page+1}")],
        [InlineKeyboardButton(text="📝Tahrirlash", callback_data=f"bedit:{id_}")],
        [InlineKeyboardButton(text="❌O'chirish", callback_data=f"bdelete:{id_}")]
    ])

async def bdelete_confirm(id_):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌", callback_data=f"cbdelete:none"), InlineKeyboardButton(text="✅", callback_data=f"cbdelete:{id_}")]
    ])


async def edit_birthday(id_):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Tug'ilgan kun", callback_data=f"edit:1:{id_}"), InlineKeyboardButton(text="Rasm", callback_data=f"edit:2:{id_}")],
        [InlineKeyboardButton(text="Ism", callback_data=f"edit:3:{id_}"), InlineKeyboardButton(text="Familiya", callback_data=f"edit:4:{id_}")],
        [InlineKeyboardButton(text="Sharif", callback_data=f"edit:5:{id_}")],
        [InlineKeyboardButton(text="Tugatish ✅", callback_data=f"edit:6:{id_}")]
    ])