from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    """lowprice states"""
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
    """highprice states"""
    city_h = State()
    location_id_h = State()
    reply_city_h = State()
    date_begin_h = State()
    date_begin_callback_h = State()
    confirm_h = State()
    date_finish_h = State()
    confirm_2_h = State()
    amount_hostels_h = State()
    is_photo_h = State()
    amount_photo_h = State()
    """bestdeal states"""
    city_b = State()
    location_id_b = State()
    reply_city_b = State()
    date_begin_b = State()
    date_begin_callback_b = State()
    confirm_b = State()
    date_finish_b = State()
    confirm_2_b = State()
    amount_hostels_b = State()
    price_range = State()
    price_min = State()
    price_max = State()
    distance = State()
    distance_confirm = State()
    distance_min = State()
    distance_max = State()
    amount_hostels_d = State()
    is_photo_d = State()
    amount_photo_d = State()
    """history states"""
    date_start_1 = State()
    date_start_2 = State()
    date_end_1 = State()
    date_end_2 = State()
    search_history = State()




