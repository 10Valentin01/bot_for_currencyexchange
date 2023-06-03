from aiogram.dispatcher.filters.state import State, StatesGroup

class adminka(StatesGroup):
    text_message = State()
    text_btn = State()
    url = State()
    mail = State()
    photo = State()
    pre_end = State()
    adminka_2 = State()

class rub(StatesGroup):
    ru = State()

class uah(StatesGroup):
    ua = State()