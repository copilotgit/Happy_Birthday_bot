from aiogram.fsm.state import State, StatesGroup

class edit_birth(StatesGroup):
    birthday1 = State()
    birthday2 = State()
    birthday3 = State()
    rasm = State()
    name = State()
    surname= State()
    patronymic = State()
    tasdiqlash = State()