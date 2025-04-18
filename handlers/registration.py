from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states.registration import register
from keyboards.inline_kb import *
from utils.Database import Database
from filters.IsGroup import IsGroup
from data.config import *
from aiogram.utils.deep_linking import create_start_link, decode_payload
from datetime import datetime

bot = Bot(TOKEN)
dp = Router()
db = Database()

@dp.callback_query(F.data == "bekor_qilish")
async def bekor_qilish(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.delete()
    await callback.message.answer("Bekor qilindi ❌")
    await state.clear()


@dp.message(IsGroup(F, BOT_NAME), Command("register"))
async def register_(message: Message, state: FSMContext):
    link = await create_start_link(bot, payload=f"group_id:{message.chat.id}", encode = True)
    await message.answer("Ro'yxatdan o'tkazish uchun bosing 👇", reply_markup=await bosing(link))
    
@dp.message(Command("register"))
async def private_register(message: Message):
    await message.answer("Bu bot faqat guruhda ishlaydi.Boni biror guruhga qo'shing, so'ngra qayta /register ni bosing!")

@dp.message(F.text.startswith("/start"))
async def start_cmmd(message: Message, state: FSMContext):
    try:
        group_id = decode_payload(message.text.split(" ", maxsplit=1)[1])
        print(group_id)
        await state.update_data(group_id = group_id)
        await message.answer("Yaxshi, ismingizni kiriting")
        await state.set_state(register.name)
    except:
        await message.answer("Assalomu alaykum, It's my birthday bot ga xush kelibsiz")

@dp.message(register.name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer("Yaxshi, endi familiyangizni kiriting")
    await state.set_state(register.surname)

@dp.message(register.surname)
async def reg_surname(message: Message, state: FSMContext):
    await state.update_data(surname = message.text)
    await message.answer("Yaxshi, endi otangizni ismini kiriting")
    await state.set_state(register.patronymic)

@dp.message(register.patronymic)
async def reg_age(message: Message, state: FSMContext):
    await state.update_data(patronymic = message.text)
    await message.answer("Yaxshi, endi rasmingizni yuboring")
    await state.set_state(register.rasm)

@dp.message(register.rasm)
async def reg_rasm(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(picture = message.photo[-1].file_id)
        await message.answer("Yaxshi, tug'ilgan kuningizni kiriting(kk-oo-yyyy formatida)\n\n<b>M: 05-05-2025</b>\n\n<u>☐</u>☐-☐☐-☐☐☐☐", reply_markup=await klaviatura(), parse_mode="HTML")   
        await state.set_state(register.birthday1)
    else:
        await message.answer("Iltimos rasm yuboring")
    

@dp.callback_query(register.birthday1)
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
        await state.set_state(register.birthday2)
        return
    elif len(num) == 2 and (int(num) > 31 or int(num) <= 0):
        await callback.message.edit_text("❗️Iltimos, to'g'ri formatda kiriting\n\n<b>M: 05-05-2025</b>\n\n<u>☐</u>☐-☐☐-☐☐☐☐", reply_markup=await klaviatura(), parse_mode="HTML")
        return
    await callback.message.edit_text(f"{num}<u>☐</u>-☐☐-☐☐☐☐", reply_markup=await klaviatura(num))

@dp.callback_query(register.birthday2)
async def reg_birthday2(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    num = (await state.get_data()).get("num")
    oy =  callback.data.split(":")[1]
    if oy == "100":
        await callback.message.edit_text(f"{num[0]}<u>☐</u>-☐☐-☐☐☐☐", reply_markup=await klaviatura(num[0]))
        await state.set_state(register.birthday1)
        return
    bir = ["01", "03", "05", "07", "08", "10", "12"]
    nol = ["04", "06", "09", "11"]
    if (oy in bir and int(num) > 31 ) or (oy in nol and int(num) > 30) or (oy == "02" and int(num) > 29):
        await callback.message.edit_text(f"❗️Bunday sana mavjud emas: {num}-{oy}\n\n<u>☐</u>☐-☐☐-☐☐☐☐", reply_markup=await klaviatura(), parse_mode="HTML")
        await state.set_state(register.birthday1)
        return

    await callback.message.edit_text(f"{num}-{oy}-<u>☐</u>☐☐☐", reply_markup=await klaviatura())
    await state.update_data(oy = oy)
    await state.set_state(register.birthday3)

@dp.callback_query(register.birthday3)
async def reg_birthday3(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    num = (await state.get_data()).get("num")
    oy = (await state.get_data()).get("oy")
    year = callback.data.split(":")[1]
    if year.startswith("none/"):
        year = year.split("/")[1]
        if not year:
            await callback.message.edit_text(f"{num}-<u>☐☐</u>-☐☐☐☐", reply_markup=klaviatura_oy)
            await state.set_state(register.birthday2)
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
        data = await state.get_data()
        await callback.message.delete()
        await callback.message.answer_photo(photo=data["picture"], caption = f"Sizning ma'lumotlaringiz 👇\nI{data['name']} {data['surname']} {data['patronymic']}\nTug'ilgan kuningiz:\n{num}-{oy}-{year}", reply_markup=tasdiqlash)
        await state.update_data(year = year)
        await state.update_data(birthday = f"{num}-{oy}-{year}")
        await state.set_state(register.tasdiqlash)

        # await state.set_state(register.tasdiqlash)

@dp.callback_query(register.tasdiqlash)
async def reg_tasdiq(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()    
    if callback.data == "ha":
        await callback.message.delete()
        db.up_data(callback.message.chat.id, data["name"], data["surname"], data["patronymic"], data["picture"], data["birthday"], data["group_id"])
        print(data)
        await callback.message.answer("Tasdiqlandi ✅")
        await state.clear()
    elif callback.data == "qaytib":
        await callback.message.delete()
        num = data["num"]
        oy = data["oy"]
        year = data["year"]
        await callback.message.answer(f"{num}-{oy}-{year[:3]}<u>☐</u>", reply_markup=await klaviatura(year[:3]))
        await state.set_state(register.birthday3)
    else:
        await callback.message.delete()
        await callback.message.answer("Bekor qilindi ❌")
        await state.clear()
