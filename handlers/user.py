from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from filters.IsGroup import IsGroup, IsPrivate
from data.config import BOT_NAME
from utils.Database import Database
from keyboards.inline_kb import *
from states.edit_birthday import edit_birth
from datetime import datetime

db = Database()
dp = Router()

@dp.message(IsGroup(F, BOT_NAME), Command("list_birthdays"))
async def list_birthdays(message: Message):
    data = db.get_birthdays(str(message.chat.id))
    if not data:
        await message.answer("Bu guruhda hali hech kim ro'yxatdan o'tmagan.\nRo'yxatdan o'tish uchun /register buyrug'ini bosing")
        return
    await message.answer_photo(photo = data[0][5], caption = f"{data[0][3]} {data[0][2]} {data[0][4]}\nTug'ilgan kun:\n{data[0][6]}", reply_markup=await paginate_birthdays(0))

@dp.callback_query(F.data.startswith("page:"))
async def paginate(callback: CallbackQuery, state: FSMContext):
    data = db.get_birthdays(str(callback.message.chat.id))
    page = int(callback.data.split(":")[1])
    if page < 0 or page >= len(data):
        await callback.answer("❗Bu sahifa mavjud emas❗")
        return
    await callback.message.delete()
    await callback.message.answer_photo(photo = data[page][5], caption = f"{data[page][3]} {data[page][2]} {data[page][4]}\nTug'ilgan kun:\n{data[page][6]}", reply_markup=await paginate_birthdays(page))


@dp.message(IsPrivate(), Command("my_birthdays"))
async def list_birthdays(message: Message):
    data = db.get_birthdays_by_user(str(message.from_user.id))
    if not data:
        await message.answer("Siz hali hech kimni ro'yxatdan o'tkazmagansiz!\nRo'yxatdan o'tish uchun /register buyrug'ini bosing")
        return
    await message.answer_photo(photo = data[0][5], caption = f"{data[0][3]} {data[0][2]} {data[0][4]}\nTug'ilgan kun:\n{data[0][6]}", reply_markup=await paginate_my_birthdays(0, data[0][0]))

@dp.callback_query(F.data.startswith("bpage:"))
async def paginate(callback: CallbackQuery, state: FSMContext):
    data = db.get_birthdays_by_user(str(callback.message.chat.id))
    print(data)
    page = int(callback.data.split(":")[1])
    if page < 0 or page >= len(data):
        await callback.answer("❗Bu sahifa mavjud emas❗")
        return
    await callback.message.delete()
    await callback.message.answer_photo(photo = data[page][5], caption = f"{data[page][3]} {data[page][2]} {data[page][4]}\nTug'ilgan kun:\n{data[page][6]}", reply_markup=await paginate_my_birthdays(page, data[page][0]))

@dp.callback_query(F.data.startswith("bdelete:"))
async def delete_birthday_c(callback: CallbackQuery, state: FSMContext):
    id_ = int(callback.data.split(":")[1])
    await callback.answer("")
    await callback.message.edit_caption(caption="Rostdan ham o'chirmoqchimisiz?", reply_markup = await bdelete_confirm(id_))
    
@dp.callback_query(F.data.startswith("cbdelete:"))
async def delete_birthday_cc(callback: CallbackQuery, state: FSMContext):
    id_ = (callback.data.split(":")[1])
    await callback.answer("")
    if id_ == "none":
        await callback.message.delete()
        await callback.message.answer("Bekor qilindi ❌👌")
        return
    db.delete_birthday(int(id_))
    await callback.message.delete()
    await callback.message.answer("O'chirildi \n🌹\n🫰")

@dp.callback_query(F.data.startswith("bedit:"))
async def edit_birthday_def(callback: CallbackQuery, state: FSMContext):
    id_ = int(callback.data.split(":")[1])
    await callback.answer("")
    await callback.message.edit_caption(caption="Nimani tahrirlamoqchisiz?", reply_markup=await edit_birthday(id_))

@dp.callback_query(F.data.startswith("edit:"))
async def edit_smthng(callback: CallbackQuery, state: FSMContext):
    id_ = int(callback.data.split(":")[2])
    data = db.get_birthdays_by_user_and_id(str(callback.message.chat.id), id_)
    if not data:
        await callback.message.answer("❗Ooops, Nimadir xato ketdi❗")
        return
    data = data[0]
    tur = callback.data.split(":")[1]
    if tur.startswith("1"):
        await callback.message.delete()
        await callback.message.answer("Yaxshi, tug'ilgan kuningizni kiriting(kk-oo-yyyy formatida)\n\n<b>M: 05-05-2025</b>\n\n<u>☐</u>☐-☐☐-☐☐☐☐", reply_markup=await klaviatura(), parse_mode="HTML")   
        await state.set_state(edit_birth.birthday1)
        # pass # Tug'ilgan kun
    elif tur.startswith("2"):
        await callback.message.delete()
        await callback.message.answer("Yangi rasm yuboring: ")
        await state.set_state(edit_birth.rasm)
        # pass # Rasm
    elif tur.startswith("3"):
        await callback.message.delete()
        await callback.message.answer("Yangi ism kiriting: ")
        await state.set_state(edit_birth.name)
        # pass # Ism
    elif tur.startswith("4"):
        await callback.message.delete()
        await callback.message.answer("Yangi familiya kiriting: ")
        await state.set_state(edit_birth.surname)
        # pass # Familiya
    elif tur.startswith("5"):
        await callback.message.delete()
        await callback.message.answer("Yangi sharif kiriting: ")
        await state.set_state(edit_birth.patronymic)
        # pass # Sharif
    elif tur.startswith("6"):
        await callback.message.delete()
        await callback.message.answer("Saqlandi ✅")
        await state.clear()
        return
    await state.update_data(id_ = id_)



# @dp.callback_query(edit_birth.birthday1)
# async def edit_birthday_1(callback: CallbackQuery, state: FSMContext):
#     await callback.message.delete()
#     await callback.message.answer("Yaxshi, tug'ilgan kuningizni kiriting(kk-oo-yyyy formatida)\n\n<b>M: 05-05-2025</b>\n\n<u>☐</u>☐-☐☐-☐☐☐☐", reply_markup=await klaviatura(), parse_mode="HTML")   
#     await state.set_state(edit_birth.birthday1)

@dp.callback_query(edit_birth.birthday1)
async def reg_birthday(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    num = callback.data.split(":")[1]
    if num.startswith("none"):
        try:
            await callback.message.edit_text(f"<u>☐</u>☐-☐☐-☐☐☐☐", reply_markup=await klaviatura())
        except:
            pass
        finally:
            return
            
    if len(num) == 2 and int(num) <= 31 and int(num) > 0:
        await state.update_data(num = num)
        await callback.message.edit_text(f"{num}-<u>☐☐</u>-☐☐☐☐", reply_markup=klaviatura_oy)
        await state.set_state(edit_birth.birthday2)
        return
    elif len(num) == 2 and (int(num) > 31 or int(num) <= 0):
        await callback.message.edit_text("❗️Iltimos, to'g'ri formatda kiriting\n\n<b>M: 05-05-2025</b>\n\n<u>☐</u>☐-☐☐-☐☐☐☐", reply_markup=await klaviatura(), parse_mode="HTML")
        return
    await callback.message.edit_text(f"{num}<u>☐</u>-☐☐-☐☐☐☐", reply_markup=await klaviatura(num))

@dp.callback_query(edit_birth.birthday2)
async def reg_birthday2(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    num = (await state.get_data()).get("num")
    oy =  callback.data.split(":")[1]
    if oy == "100":
        await callback.message.edit_text(f"{num[0]}<u>☐</u>-☐☐-☐☐☐☐", reply_markup=await klaviatura(num[0]))
        await state.set_state(edit_birth.birthday1)
        return
    bir = ["01", "03", "05", "07", "08", "10", "12"]
    nol = ["04", "06", "09", "11"]
    if (oy in bir and int(num) > 31 ) or (oy in nol and int(num) > 30) or (oy == "02" and int(num) > 29):
        await callback.message.edit_text(f"❗️Bunday sana mavjud emas: {num}-{oy}\n\n<u>☐</u>☐-☐☐-☐☐☐☐", reply_markup=await klaviatura(), parse_mode="HTML")
        await state.set_state(edit_birth.birthday1)
        return

    await callback.message.edit_text(f"{num}-{oy}-<u>☐</u>☐☐☐", reply_markup=await klaviatura())
    await state.update_data(oy = oy)
    await state.set_state(edit_birth.birthday3)

@dp.callback_query(edit_birth.birthday3)
async def reg_birthday3(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    num = (await state.get_data()).get("num")
    oy = (await state.get_data()).get("oy")
    year = callback.data.split(":")[1]
    if year.startswith("none/"):
        year = year.split("/")[1]
        if not year:
            await callback.message.edit_text(f"{num}-<u>☐☐</u>-☐☐☐☐", reply_markup=klaviatura_oy)
            await state.set_state(edit_birth.birthday2)
            return
        if len(year) == 1:
            await callback.message.edit_text(f"{num}-{oy}-<u>☐</u>☐☐☐", reply_markup=await klaviatura())
        elif len(year) == 2:
            await callback.message.edit_text(f"{num}-{oy}-{year[0]}<u>☐</u>☐☐", reply_markup=await klaviatura(year[0]))
        elif len(year) == 3:
            await callback.message.edit_text(f"{num}-{oy}-{year[0:2]}<u>☐</u>☐", reply_markup=await klaviatura(year[0:2]))
        return
    if ((len(year) == 4) and ((int(year) > int(datetime.now().strftime("%Y"))) or int(year) < 1908)):
        await callback.message.edit_text(f"❗ Yaroqsiz sana kiritildi: {num}-{oy}-{year}\nQayta kiriting:\n{num}-{oy}-<u>☐</u>☐☐☐", reply_markup = await klaviatura())
        return

    if len(year) == 1:
        await callback.message.edit_text(f"{num}-{oy}-{year}<u>☐</u>☐☐", reply_markup=await klaviatura(year))
    elif len(year) == 2:
        await callback.message.edit_text(f"{num}-{oy}-{year}<u>☐</u>☐", reply_markup=await klaviatura(year))
    elif len(year) == 3:
        await callback.message.edit_text(f"{num}-{oy}-{year}<u>☐</u>", reply_markup=await klaviatura(year))
    elif len(year) == 4:
        id_ = (await state.get_data()).get("id_")
        data = db.get_birthdays_by_user_and_id(str(callback.message.chat.id), id_)
        print("NIAMDDIWMIWDIWJ",data,"|",str(callback.message.chat.id),"|",id_)
        await callback.message.delete()
        await callback.message.answer_photo(photo=data[0][5], caption = f"Sizning ma'lumotlaringiz 👇\nI{data[0][2]} {data[0][3]} {data[0][4]}\nTug'ilgan kuningiz:\n{num}-{oy}-{year}", reply_markup=tasdiqlash_year)
        await state.update_data(year = year)
        await state.update_data(birthday = f"{num}-{oy}-{year}")
        await state.set_state(edit_birth.tasdiqlash)

@dp.callback_query(edit_birth.tasdiqlash)
async def tasdiqlash_yearr(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.answer("")
    if callback.data == "yha":
        await callback.message.delete()
        # db.up_data(callback.message.chat.id, data["name"], data["surname"], data["patronymic"], data["picture"], data["birthday"], data["group_id"])
        db.update_birthday(data["birthday"], data["id_"])
        await callback.message.answer("Tasdiqlandi ✅")
        await state.clear()
    elif callback.data == "yqaytib":
        await callback.message.delete()
        num = data["num"]
        oy = data["oy"]
        year = data["year"]
        await callback.message.answer(f"{num}-{oy}-{year[:3]}<u>☐</u>", reply_markup=await klaviatura(year[:3]))
        await state.set_state(edit_birth.birthday3)
    else:
        await callback.message.delete()
        await callback.message.answer("Bekor qilindi ❌")
        await state.clear()

        # await state.set_state(register.tasdiqlash)

@dp.message(edit_birth.rasm)
async def edit_rasm(message: Message, state: FSMContext):
    if message.photo:
        id_ = (await state.get_data()).get("id_")
        data = db.get_birthdays_by_user_and_id(str(message.from_user.id), id_)
        if not data:
            await message.answer("❗Oops, Nimadir xato ketdi❗")
            return
        data = data[0]
        db.update_pic(message.photo[-1].file_id, id_)
        await message.answer_photo(photo= message.photo[-1].file_id, caption= f"{data[3]} {data[2]} {data[4]}\nTug'ilgan kun:\n{data[6]}", reply_markup=await edit_birthday(id_))
        await state.clear()
    else:
        await message.answer("Iltimos rasm yuboring")


@dp.message(edit_birth.name)
async def edit_name_def(message: Message, state: FSMContext):
    id_ = (await state.get_data()).get("id_")
    data = db.get_birthdays_by_user_and_id(str(message.from_user.id), id_)
    if not data:
        await message.answer("❗Ooops, Nimadir xato ketdi❗")
        return
    data = data[0]
    db.update_name(message.text, id_)
    await message.answer_photo(photo= data[5], caption= f"{data[3]} {message.text} {data[4]}\nTug'ilgan kun:\n{data[6]}", reply_markup=await edit_birthday(id_))
    await state.clear()

@dp.message(edit_birth.surname)
async def edit_surname_def(message: Message, state: FSMContext):
    id_ = (await state.get_data()).get("id_")
    data = db.get_birthdays_by_user_and_id(str(message.from_user.id), id_)
    if not data: 
        await message.answer("❗Ooops, Nimadir xato ketdi❗") 
        return
    data = data[0]
    db.update_surname(message.text, id_)
    await message.answer_photo(photo= data[5], caption= f"{message.text} {data[2]} {data[4]}\nTug'ilgan kun:\n{data[6]}", reply_markup=await edit_birthday(id_))
    await state.clear()

@dp.message(edit_birth.patronymic)
async def edit_patronymic_def(message: Message, state: FSMContext):
    id_ = (await state.get_data()).get("id_")
    data = db.get_birthdays_by_user_and_id(str(message.from_user.id), id_)
    if not data:
        await message.answer("❗Ooops, Nimadir xato ketdi❗")
        return
    data= data[0]
    db.update_patronymic(message.text, id_)
    await message.answer_photo(photo= data[5], caption= f"{data[3]} {data[2]} {message.text}\nTug'ilgan kun:\n{data[6]}", reply_markup=await edit_birthday(id_))
    await state.clear()

