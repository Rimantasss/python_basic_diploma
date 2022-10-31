from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    """
    Класс состояний пользователя
    Lowprice, Highprice, Bestdeal states
    """
    city = State()
    location_id = State()
    reply_city = State()
    date_begin = State()
    date_begin_callback = State()
    confirm = State()
    date_finish = State()
    confirm_2 = State()
    price_range = State()
    price_min = State()
    price_max = State()
    distance = State()
    distance_confirm = State()
    distance_min = State()
    distance_max = State()
    confirm_3 = State()
    amount_hostels = State()
    is_photo = State()
    amount_photo = State()
    """History states"""
    date_start_1 = State()
    date_start_2 = State()
    date_end_1 = State()
    date_end_2 = State()
    search_history = State()




