from aiogram.fsm.state import State, StatesGroup

class register(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()
    rasm = State()
    birthday1 = State()
    birthday2 = State()
    birthday3 = State()
    tasdiqlash = State()
