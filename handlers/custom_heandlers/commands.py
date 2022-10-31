from loader import bot
from telebot.types import Message, InputMediaPhoto, CallbackQuery
from utils.misc.search_dest_id import city_founding
from utils.misc.search_hostels import founding_hostels
from utils.misc.search_photos import founding_photo
from states.user_states import MyStates
from keyboards.inline.keyboard import yes_or_no, confirm, enter_date_start, enter_date_finish, amount_photo, link_button
from keyboards.inline.calendar import create_calendar
from database.data_base import write_database
from datetime import date, timedelta
import time


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(chat_id=message.from_user.id, state=MyStates.city, user_id=message.chat.id)
    bot.send_message(chat_id=message.from_user.id, text='В каком городе ищем?')

    with bot.retrieve_data(chat_id=message.from_user.id, user_id=message.chat.id) as data:
        data['date'] = date.today()
        data['time'] = time.strftime('%H:%M:%S')
        data['command'] = message.text[1:]


@bot.message_handler(commands=['highprice'])
def highprice(message: Message) -> None:
    bot.set_state(chat_id=message.from_user.id, state=MyStates.city, user_id=message.chat.id)
    bot.send_message(chat_id=message.from_user.id, text='В каком городе ищем?')

    with bot.retrieve_data(chat_id=message.from_user.id, user_id=message.chat.id) as data:
        data['date'] = date.today()
        data['time'] = time.strftime('%H:%M:%S')
        data['command'] = message.text[1:]


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: Message) -> None:
    bot.set_state(chat_id=message.from_user.id, state=MyStates.city, user_id=message.chat.id)
    bot.send_message(chat_id=message.from_user.id, text='В каком городе ищем?')

    with bot.retrieve_data(chat_id=message.from_user.id, user_id=message.chat.id) as data:
        data['date'] = date.today()
        data['time'] = time.strftime('%H:%M:%S')
        data['command'] = message.text[1:]


@bot.message_handler(state=MyStates.city)
def city(message: Message) -> None:
    if message.text.isalpha():
        bot.set_state(chat_id=message.from_user.id, state=MyStates.location_id, user_id=message.chat.id)

        with bot.retrieve_data(chat_id=message.from_user.id, user_id=message.chat.id) as data:
            data['city'] = message.text

        if city_founding(data['city']):
            bot.send_message(
                chat_id=message.from_user.id,
                text='Уточните, пожалуйста:',
                reply_markup=city_founding(data['city'])
            )
        else:
            bot.send_animation(
                chat_id=message.from_user.id,
                animation='https://i.gifer.com/YmvJ.gif',
                caption='По вашему запросу ничего не найдено. Попробуйте еще раз!'
            )

    else:
        bot.send_message(chat_id=message.from_user.id, text='Назвние города должно состоять только из букв!')


@bot.callback_query_handler(state=MyStates.location_id, func=None)
def select_location(callback: CallbackQuery) -> None:
    bot.set_state(chat_id=callback.from_user.id, state=MyStates.reply_city, user_id=callback.message.chat.id)
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)

    for i_call in callback.message.reply_markup.keyboard:
        for keyboard in i_call:
            if keyboard.callback_data == callback.data:
                bot.send_message(
                    chat_id=callback.from_user.id,
                    text='Вы выбрали {}, верно?'.format(keyboard.text),
                    reply_markup=yes_or_no()
                )

    with bot.retrieve_data(chat_id=callback.from_user.id, user_id=callback.message.chat.id) as data:
        data['location_id'] = callback.data


@bot.callback_query_handler(state=MyStates.reply_city, func=None)
def select_date(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    if callback.data == 'Да':
        bot.set_state(chat_id=callback.from_user.id, state=MyStates.date_begin, user_id=callback.message.chat.id)
        bot.send_message(chat_id=callback.from_user.id, text='Переходим к дате', reply_markup=enter_date_start())
    else:
        bot.set_state(chat_id=callback.from_user.id, state=MyStates.city, user_id=callback.message.chat.id)
        bot.send_message(chat_id=callback.from_user.id, text='Выберем заново...В каком городе ищем?')


@bot.callback_query_handler(state=MyStates.date_begin, func=None)
def calendar_1(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    bot.set_state(chat_id=callback.from_user.id, state=MyStates.date_begin_callback, user_id=callback.message.chat.id)
    calendar, step = create_calendar(callback_data=callback)
    bot.send_message(chat_id=callback.from_user.id, text='Введите {}'.format(step), reply_markup=calendar)


@bot.callback_query_handler(state=MyStates.date_begin_callback, func=None)
def get_date_start(callback: CallbackQuery) -> None:
    result, key, step = create_calendar(callback_data=callback, is_process=True)
    if not result and key:
        bot.edit_message_text(
            text='Введите {}'.format(step),
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=key
        )
    elif result:
        bot.edit_message_text(
            text='Ваша дата заезда: {}'.format(result),
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=enter_date_finish()
        )

        with bot.retrieve_data(chat_id=callback.from_user.id, user_id=callback.message.chat.id) as data:
            data['date_begin'] = result

        bot.set_state(chat_id=callback.from_user.id, state=MyStates.confirm, user_id=callback.message.chat.id)


@bot.callback_query_handler(state=MyStates.confirm, func=None)
def calendar_2(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)

    with bot.retrieve_data(chat_id=callback.from_user.id, user_id=callback.message.chat.id) as data:
        min_date = data['date_begin']

    bot.set_state(chat_id=callback.from_user.id, state=MyStates.date_finish, user_id=callback.message.chat.id)
    calendar, step = create_calendar(callback_data=callback, min_date=min_date)
    bot.send_message(chat_id=callback.from_user.id, text='Введите {}'.format(step), reply_markup=calendar)


@bot.callback_query_handler(state=MyStates.date_finish, func=None)
def get_date_finish(callback: CallbackQuery) -> None:

    with bot.retrieve_data(chat_id=callback.from_user.id, user_id=callback.message.chat.id) as data:
        min_date = data['date_begin'] + timedelta(days=1)

    result, key, step = create_calendar(callback_data=callback, min_date=min_date, is_process=True)
    if not result and key:
        bot.edit_message_text(
            text='Введите {}'.format(step),
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=key
        )
    elif result:
        bot.edit_message_text(
            text='Ваша дата отъезда: {}'.format(result),
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=confirm()
        )
        with bot.retrieve_data(chat_id=callback.from_user.id, user_id=callback.message.chat.id) as data:
            amt_days = str(result - data['date_begin'])
            only_days = amt_days.split()[0]
            data['amount_days'] = int(only_days)
            if data['command'] == 'bestdeal':
                bot.set_state(chat_id=callback.from_user.id, state=MyStates.confirm_2, user_id=callback.message.chat.id)
            else:
                bot.set_state(chat_id=callback.from_user.id, state=MyStates.confirm_3, user_id=callback.message.chat.id)


@bot.callback_query_handler(state=MyStates.confirm_2, func=None)
def select_prices(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    bot.set_state(chat_id=callback.from_user.id, state=MyStates.price_range, user_id=callback.message.chat.id)
    bot.send_message(chat_id=callback.from_user.id, text='Теперь выберем диапозон цен', reply_markup=confirm())


@bot.callback_query_handler(state=MyStates.price_range, func=None)
def enter_price(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    bot.set_state(chat_id=callback.from_user.id, state=MyStates.price_max, user_id=callback.message.chat.id)
    bot.send_message(chat_id=callback.from_user.id, text='Напишите минимальную цену ($) за сутки')


@bot.message_handler(state=MyStates.price_max)
def get_price_min(message: Message) -> None:
    if message.text.isdecimal():
        bot.set_state(chat_id=message.from_user.id, state=MyStates.distance, user_id=message.chat.id)
        bot.send_message(chat_id=message.from_user.id, text='Напишите максимальную цену ($) за сутки')

        with bot.retrieve_data(chat_id=message.from_user.id, user_id=message.chat.id) as data:
            data['price_min'] = message.text

    else:
        bot.send_message(chat_id=message.from_user.id, text='Введите цифрами!')


@bot.message_handler(state=MyStates.distance)
def get_price_max(message: Message) -> None:
    if message.text.isdecimal():
        bot.set_state(chat_id=message.from_user.id, state=MyStates.distance_confirm, user_id=message.chat.id)
        bot.send_message(
            chat_id=message.from_user.id,
            text='Теперь выберем диапозон расстояний',
            reply_markup=confirm()
        )

        with bot.retrieve_data(chat_id=message.from_user.id, user_id=message.chat.id) as data:
            data['price_max'] = message.text


@bot.callback_query_handler(state=MyStates.distance_confirm, func=None)
def select_distance(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    bot.set_state(chat_id=callback.from_user.id, state=MyStates.distance_min, user_id=callback.message.chat.id)
    bot.send_message(chat_id=callback.from_user.id, text='Напишите минимальное расстояние (км) от центра')


@bot.message_handler(state=MyStates.distance_min)
def get_distance_min(message: Message) -> None:
    if message.text.isdecimal():
        bot.set_state(chat_id=message.from_user.id, state=MyStates.distance_max, user_id=message.chat.id)
        bot.send_message(chat_id=message.from_user.id, text='Напишите максимальное расстояние (км) от центра')

        with bot.retrieve_data(chat_id=message.from_user.id, user_id=message.chat.id) as data:
            data['distance_min'] = float(message.text)

    else:
        bot.send_message(chat_id=message.from_user.id, text='Введите цифрами!')


@bot.message_handler(state=MyStates.distance_max)
def get_distance_max(message: Message) -> None:
    if message.text.isdecimal():
        bot.set_state(chat_id=message.from_user.id, state=MyStates.amount_hostels, user_id=message.chat.id)
        bot.send_message(chat_id=message.from_user.id, text='Сколько отелей показать?')

        with bot.retrieve_data(chat_id=message.from_user.id, user_id=message.chat.id) as data:
            data['distance_max'] = float(message.text)

    else:
        bot.send_message(chat_id=message.from_user.id, text='Введите цифрами!')


@bot.callback_query_handler(state=MyStates.confirm_3, func=None)
def amount_hostels(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    bot.set_state(chat_id=callback.from_user.id, state=MyStates.amount_hostels, user_id=callback.message.chat.id)

    with bot.retrieve_data(chat_id=callback.from_user.id, user_id=callback.message.chat.id) as data:
        if data['command'] != 'bestdeal':
            bot.send_message(chat_id=callback.from_user.id, text='Сколько отелей показать?')


@bot.message_handler(state=MyStates.amount_hostels)
def get_amount_hostels(message: Message) -> None:
    if message.text.isdecimal():
        bot.set_state(chat_id=message.from_user.id, state=MyStates.is_photo, user_id=message.chat.id)
        bot.send_message(
            chat_id=message.from_user.id,
            text='Загрузить фото?',
            reply_markup=yes_or_no())

        with bot.retrieve_data(chat_id=message.from_user.id, user_id=message.chat.id) as data:
            data['amount_hostels'] = int(message.text)

    else:
        bot.send_message(chat_id=message.from_user.id, text='Введите цифрами!')


@bot.callback_query_handler(state=MyStates.is_photo, func=None)
def is_photo(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    if callback.data == 'Да':
        bot.set_state(chat_id=callback.from_user.id, state=MyStates.amount_photo, user_id=callback.message.chat.id)
        bot.send_message(chat_id=callback.from_user.id, text='Сколько фото загрузить?', reply_markup=amount_photo())
    else:
        with bot.retrieve_data(chat_id=callback.from_user.id, user_id=callback.message.chat.id) as data:
            if data['command'] == 'bestdeal':
                id_hostels_list, info_hostel_list, all_hostels_name, link = founding_hostels(
                    data['location_id'], data['amount_hostels'], data['amount_days'], 'bestdeal',
                    data['price_min'], data['price_max'], data['distance_min'], data['distance_max']
                )
            else:
                id_hostels_list, info_hostel_list, all_hostels_name, link = founding_hostels(
                    data['location_id'], data['amount_hostels'], data['amount_days'], data['command']
                )
            write_database(data['command'], data['date'], data['time'], all_hostels_name)

        for i_id_hostel in enumerate(info_hostel_list):
            num, i_id = i_id_hostel
            bot.send_message(chat_id=callback.from_user.id, text=i_id, reply_markup=link_button(link[num]))


@bot.callback_query_handler(state=MyStates.amount_photo, func=None)
def get_all_info(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    with bot.retrieve_data(chat_id=callback.from_user.id, user_id=callback.message.chat.id) as data:
        data['amount_photo'] = int(callback.data)

    if data['command'] == 'bestdeal':
        id_hostels_list, info_hostel_list, all_hostels_name, link = founding_hostels(
            data['location_id'], data['amount_hostels'], data['amount_days'], 'bestdeal',
            data['price_min'], data['price_max'], data['distance_min'], data['distance_max']
        )
    else:
        id_hostels_list, info_hostel_list, all_hostels_name, link = founding_hostels(
            data['location_id'], data['amount_hostels'], data['amount_days'], data['command']
        )

    for i_id_hostel in enumerate(id_hostels_list):
        num, i_id = i_id_hostel
        pics = founding_photo(i_id, data['amount_photo'])
        bot.send_media_group(
            chat_id=callback.from_user.id,
            media=[InputMediaPhoto(i_pic) for i_pic in pics]
        )
        bot.send_message(chat_id=callback.from_user.id, text=info_hostel_list[num], reply_markup=link_button(link[num]))
        bot.set_state(chat_id=callback.from_user.id, state=None, user_id=callback.message.chat.id)

    write_database(data['command'], data['date'], data['time'], all_hostels_name)
