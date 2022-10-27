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


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    bot.send_message(message.from_user.id, 'В каком городе ищем?')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['date'] = date.today()
        data['time'] = time.strftime('%H:%M:%S')


@bot.message_handler(state=MyStates.city)
def city(message: Message) -> None:
    if message.text.isalpha():
        bot.set_state(message.from_user.id, MyStates.location_id, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text

        bot.send_message(
            message.from_user.id,
            'Уточните, пожалуйста:',
            reply_markup=city_founding(data['city'])
        )

    else:
        bot.send_message(message.chat.id, 'Назвние города должно состоять только из букв!')


@bot.callback_query_handler(state=MyStates.location_id, func=None)
def worker_callback_2(callback: CallbackQuery) -> None:
    bot.set_state(callback.from_user.id, MyStates.reply_city, callback.message.chat.id)
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


@bot.callback_query_handler(state=MyStates.reply_city, func=None)
def worker_callback_3(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.date_begin, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, text='Переходим к дате', reply_markup=enter_date_start())
    else:
        bot.set_state(callback.from_user.id, MyStates.city, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, 'Выберем заново...В каком городе ищем?')


@bot.callback_query_handler(state=MyStates.date_begin, func=None)
def worker_callback_4(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.date_begin_callback, callback.message.chat.id)
        calendar, step = create_calendar(callback_data=callback)
        bot.send_message(callback.message.chat.id, 'Введите {}'.format(step), reply_markup=calendar)


@bot.callback_query_handler(state=MyStates.date_begin_callback, func=None)
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

        bot.set_state(callback.from_user.id, MyStates.confirm, callback.message.chat.id)


@bot.callback_query_handler(state=MyStates.confirm, func=None)
def worker_callback_6(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)

    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        min_date = data['date_begin']

    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.date_finish, callback.message.chat.id)
        calendar, step = create_calendar(callback_data=callback, min_date=min_date)
        bot.send_message(callback.message.chat.id, 'Введите {}'.format(step), reply_markup=calendar)


@bot.callback_query_handler(state=MyStates.date_finish, func=None)
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
        bot.set_state(callback.from_user.id, MyStates.confirm_2, callback.message.chat.id)


@bot.callback_query_handler(state=MyStates.confirm_2, func=None)
def worker_callback_8(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.amount_hostels, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, 'Сколько отелей показать?')


@bot.message_handler(state=MyStates.amount_hostels)
def get_amount_hostels(message: Message) -> None:
    if message.text.isdecimal():
        bot.set_state(message.from_user.id, MyStates.is_photo, message.chat.id)
        bot.send_message(
            chat_id=message.chat.id,
            text='Загрузить фото?',
            reply_markup=yes_or_no())

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['amount_hostels'] = int(message.text)

    else:
        bot.send_message(message.chat.id, 'Введите цифрами!')


@bot.callback_query_handler(state=MyStates.is_photo, func=None)
def worker_callback_9(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.amount_photo, callback.message.chat.id)
        bot.send_message(callback.from_user.id, 'Сколько фото загрузить?', reply_markup=amount_photo())
    else:
        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            id_hostels_list, info_hostel_list, all_hostels_name = founding_hostels(
                data['location_id'], data['amount_hostels'], data['amount_days'], 'lowprice'
            )
            write_database('lowprice', data['date'], data['time'], all_hostels_name)

        for i_id in info_hostel_list:
            bot.send_message(callback.from_user.id, i_id)


@bot.callback_query_handler(state=MyStates.amount_photo, func=None)
def get_amount_photo(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        data['amount_photo'] = int(callback.data)

    id_hostels_list, info_hostel_list, all_hostels_name = founding_hostels(
        data['location_id'], data['amount_hostels'], data['amount_days'], 'lowprice'
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

    write_database('lowprice', data['date'], data['time'], all_hostels_name)

