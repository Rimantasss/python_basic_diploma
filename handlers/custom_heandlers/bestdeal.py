from loader import bot
from telebot.types import Message, InputMediaPhoto, CallbackQuery
from utils.misc.search_dest_id import city_founding
from utils.misc.search_hostels import founding_hostels
from utils.misc.search_photos import founding_photo
from states.user_states import MyStates
from keyboards.inline.yes_or_no_buttons import yes_or_no
from keyboards.inline.confirm_buttons import confirm
from keyboards.inline.enter_date_start import enter_date_start
from keyboards.inline.amount_photo import amount_photo
from keyboards.inline.enter_date_finish import enter_date_finish
from keyboards.inline.calendar import create_calendar
from database.write_to_db import write_database
from datetime import date, timedelta
import time


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: Message) -> None:
    bot.set_state(message.from_user.id, MyStates.city_b, message.chat.id)
    bot.send_message(message.from_user.id, 'В каком городе ищем?')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['date'] = date.today()
        data['time'] = time.strftime('%H:%M:%S')


@bot.message_handler(state=MyStates.city_b)
def city(message: Message) -> None:
    if message.text.isalpha():
        bot.set_state(message.from_user.id, MyStates.location_id_b, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text

        bot.send_message(
            message.from_user.id,
            'Уточните, пожалуйста:',
            reply_markup=city_founding(data['city'])
        )

    else:
        bot.send_message(message.chat.id, 'Назвние города должно состоять только из букв!')


@bot.callback_query_handler(state=MyStates.location_id_b, func=None)
def worker_callback_2(callback: CallbackQuery) -> None:
    bot.set_state(callback.from_user.id, MyStates.reply_city_b, callback.message.chat.id)
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)

    for i_call in callback.message.reply_markup.keyboard:
        for keyboard in i_call:
            if keyboard.callback_data == callback.data:
                bot.send_message(
                    chat_id=callback.from_user.id,
                    text='Вы выбрали {}, верно?'.format(keyboard.text),
                    reply_markup=yes_or_no()
                )

    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        data['location_id'] = callback.data


@bot.callback_query_handler(state=MyStates.reply_city_b, func=None)
def worker_callback_3(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.date_begin_b, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, text='Переходим к дате', reply_markup=enter_date_start())
    else:
        bot.set_state(callback.from_user.id, MyStates.city_b, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, 'Выберем заново...В каком городе ищем?')


@bot.callback_query_handler(state=MyStates.date_begin_b, func=None)
def worker_callback_4(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.date_begin_callback_b, callback.message.chat.id)
        calendar, step = create_calendar(callback_data=callback)
        bot.send_message(callback.message.chat.id, 'Введите {}'.format(step), reply_markup=calendar)


@bot.callback_query_handler(state=MyStates.date_begin_callback_b, func=None)
def worker_callback_5(callback: CallbackQuery) -> None:
    result, key, step = create_calendar(callback_data=callback, is_process=True)
    if not result and key:
        bot.edit_message_text(
            'Введите {}'.format(step),
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=key
        )
    elif result:
        bot.edit_message_text(
            'Ваша дата заезда: {}'.format(result),
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=enter_date_finish()
        )

        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data['date_begin'] = result

        bot.set_state(callback.from_user.id, MyStates.confirm_b, callback.message.chat.id)


@bot.callback_query_handler(state=MyStates.confirm_b, func=None)
def worker_callback_6(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)

    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        min_date = data['date_begin']

    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.date_finish_b, callback.message.chat.id)
        calendar, step = create_calendar(callback_data=callback, min_date=min_date)
        bot.send_message(callback.message.chat.id, 'Введите {}'.format(step), reply_markup=calendar)


@bot.callback_query_handler(state=MyStates.date_finish_b, func=None)
def worker_callback_7(callback: CallbackQuery) -> None:
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        min_date = data['date_begin'] + timedelta(days=1)

    result, key, step = create_calendar(callback_data=callback, min_date=min_date, is_process=True)
    if not result and key:
        bot.edit_message_text(
            'Введите {}'.format(step),
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=key
        )
    elif result:
        bot.edit_message_text(
            'Ваша дата отъезда: {}'.format(result),
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=confirm()
        )
        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            amt_days = str(result - data['date_begin'])
            only_days = amt_days.split()[0]
            data['amount_days'] = int(only_days)
        bot.set_state(callback.from_user.id, MyStates.confirm_2_b, callback.message.chat.id)


@bot.callback_query_handler(state=MyStates.confirm_2_b, func=None)
def worker_callback_8(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.price_range, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, 'Теперь выберем диапозон цен', reply_markup=confirm())


@bot.callback_query_handler(state=MyStates.price_range, func=None)
def worker_callback_8(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    bot.set_state(callback.from_user.id, MyStates.price_max, callback.message.chat.id)
    bot.send_message(callback.message.chat.id, 'Напишите минимальную цену за сутки в $')


@bot.message_handler(state=MyStates.price_max)
def get_amount_hostels(message: Message) -> None:
    if message.text.isdecimal():
        bot.set_state(message.from_user.id, MyStates.distance, message.chat.id)
        bot.send_message(message.chat.id, 'Напишите максимальную цену за сутки в $')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_min'] = message.text

    else:
        bot.send_message(message.chat.id, 'Введите цифрами!')


@bot.message_handler(state=MyStates.distance)
def get_amount_hostels(message: Message) -> None:
    if message.text.isdecimal():
        bot.set_state(message.from_user.id, MyStates.distance_confirm, message.chat.id)
        bot.send_message(message.chat.id, 'Теперь выберем диапозон расстояний', reply_markup=confirm())

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_max'] = message.text


@bot.callback_query_handler(state=MyStates.distance_confirm, func=None)
def worker_callback_8(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.distance_min, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, 'Напишите минимальное расстояние (км) от центра')


@bot.message_handler(state=MyStates.distance_min)
def get_amount_hostels(message: Message) -> None:
    if message.text.isdecimal():
        bot.set_state(message.from_user.id, MyStates.distance_max, message.chat.id)
        bot.send_message(message.chat.id, 'Напишите максимальное расстояние (км) от центра')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance_min'] = float(message.text)

    else:
        bot.send_message(message.chat.id, 'Введите цифрами!')


@bot.message_handler(state=MyStates.distance_max)
def get_amount_hostels(message: Message) -> None:
    if message.text.isdecimal():
        bot.set_state(message.from_user.id, MyStates.amount_hostels_d, message.chat.id)
        bot.send_message(message.chat.id, 'Сколько отелей показать?')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance_max'] = float(message.text)

    else:
        bot.send_message(message.chat.id, 'Введите цифрами!')


@bot.message_handler(state=MyStates.amount_hostels_d)
def get_amount_hostels(message: Message) -> None:
    if message.text.isdecimal():
        bot.set_state(message.from_user.id, MyStates.is_photo_d, message.chat.id)
        bot.send_message(
            chat_id=message.chat.id,
            text='Загрузить фото?',
            reply_markup=yes_or_no())

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['amount_hostels'] = int(message.text)

    else:
        bot.send_message(message.chat.id, 'Введите цифрами!')


@bot.callback_query_handler(state=MyStates.is_photo_d, func=None)
def worker_callback_9(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.amount_photo_d, callback.message.chat.id)
        bot.send_message(callback.from_user.id, 'Сколько фото загрузить?', reply_markup=amount_photo())
    else:
        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            id_hostels_list, info_hostel_list, all_hostels_name = founding_hostels(
                data['location_id'], data['amount_hostels'], data['amount_days'], 'bestdeal',
                data['price_min'], data['price_max'], data['distance_min'], data['distance_max']
            )
            write_database('bestdeal', data['date'], data['time'], all_hostels_name)

        for i_id in info_hostel_list:
            bot.send_message(callback.from_user.id, i_id)


@bot.callback_query_handler(state=MyStates.amount_photo_d, func=None)
def get_amount_photo(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        data['amount_photo'] = int(callback.data)

    id_hostels_list, info_hostel_list, all_hostels_name = founding_hostels(
        data['location_id'], data['amount_hostels'], data['amount_days'], 'bestdeal',
        data['price_min'], data['price_max'], data['distance_min'], data['distance_max']
    )

    for i_id_hostel in enumerate(id_hostels_list):
        num, i_id = i_id_hostel
        pics = founding_photo(i_id, data['amount_photo'])
        bot.send_media_group(
            chat_id=callback.message.chat.id,
            media=[InputMediaPhoto(i_pic) for i_pic in pics]
        )
        bot.send_message(callback.message.chat.id, info_hostel_list[num])
        bot.set_state(callback.from_user.id, None, callback.message.chat.id)

    write_database('bestdeal', data['date'], data['time'], all_hostels_name)


#, data['distance_min'], data['distance_max']