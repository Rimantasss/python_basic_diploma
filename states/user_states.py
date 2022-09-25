from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    city = State()
    dest_id = State()
    amount_hostels = State()
    is_photo = State()
    amount_photo = State()



