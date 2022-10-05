from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    city = State()
    location_id = State()
    reply_city = State()
    date_begin = State()
    date_begin_callback = State()
    confirm_or_fix = State()
    confirm_or_fix_2 = State()
    date_finish = State()
    date_finish_callback = State()
    amount_hostels = State()
    is_photo = State()
    amount_photo = State()




