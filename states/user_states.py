from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    city = State()
    location_id = State()
    reply_city = State()
    date_begin = State()
    date_begin_callback = State()
    confirm = State()
    date_finish = State()
    confirm_2 = State()
    amount_hostels = State()
    is_photo = State()
    amount_photo = State()




