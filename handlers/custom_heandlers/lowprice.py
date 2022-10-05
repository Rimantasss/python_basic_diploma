from loader import bot
from telebot.types import Message, InputMediaPhoto
from utils.misc.search_dest_id import city_founding
from utils.misc.search_hostels import founding_hostels
from utils.misc.search_photos import founding_photo
from states.user_states import MyStates
from keyboards.inline.yes_or_no_buttons import yes_or_no
from keyboards.inline.confirm_buttons import confirm
from telegram_bot_calendar import DetailedTelegramCalendar


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    bot.send_message(message.from_user.id, 'В каком городе ищем?')


@bot.message_handler(state=MyStates.city)
def city(message: Message) -> None:
    if message.text.isalpha():
        bot.set_state(message.from_user.id, MyStates.location_id, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text

        bot.send_message(
            message.from_user.id, 'Уточните, пожалуйста:', reply_markup=city_founding(data['city'])
        )

    else:
        bot.send_message(message.chat.id, 'Назвние города должно состоять только из букв!')


@bot.callback_query_handler(state=MyStates.location_id, func=lambda callback: callback.data)
def worker_callback_2(callback):
    bot.set_state(callback.from_user.id, MyStates.reply_city, callback.message.chat.id)

    for i in callback.message.reply_markup.keyboard:
        for keyboard in i:
            if keyboard.callback_data == callback.data:
                bot.send_message(
                    chat_id=callback.from_user.id,
                    text='Вы выбрали {}, верно?'.format(keyboard.text),
                    reply_markup=yes_or_no())

    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        data['location_id'] = callback.data


@bot.callback_query_handler(state=MyStates.reply_city, func=lambda callback: callback.data)
def worker_callback_3(callback):
    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.date_begin, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, 'На сколько дней хотите забронировать отель?')
    else:
        bot.set_state(callback.from_user.id, MyStates.city, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, 'Выберем заново...В каком городе ищем?')


@bot.message_handler(state=MyStates.date_begin)
def date(message: Message) -> None:
    bot.set_state(message.from_user.id, MyStates.date_begin_callback, message.chat.id)
    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    bot.send_message(message.chat.id, 'Введите дату заселения', reply_markup=calendar)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['amount_days'] = int(message.text)


@bot.callback_query_handler(state=MyStates.date_begin_callback, func=DetailedTelegramCalendar.func())
def worker_callback_4(callback):
    result, key, step = DetailedTelegramCalendar(locale='ru').process(callback.data)
    if not result and key:
        bot.edit_message_text(
            'Введите дату',
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=key
        )
    elif result:
        bot.edit_message_text(
            'Ваша дата заезда: {}'.format(result),
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=confirm()
        )
        bot.set_state(callback.from_user.id, MyStates.confirm_or_fix, callback.message.chat.id)


@bot.callback_query_handler(state=MyStates.confirm_or_fix, func=lambda callback: callback.data)
def worker_callback_5(callback):
    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.date_finish_callback, callback.message.chat.id)
        calendar, step = DetailedTelegramCalendar(locale='ru').build()
        bot.send_message(callback.message.chat.id, 'Введите дату отъезда', reply_markup=calendar)


@bot.message_handler(state=MyStates.date_finish)
def date(message: Message) -> None:
    bot.set_state(message.from_user.id, MyStates.date_finish_callback, message.chat.id)
    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    bot.send_message(message.chat.id, 'Введите дату отъезда', reply_markup=calendar)


@bot.callback_query_handler(state=MyStates.date_finish_callback, func=DetailedTelegramCalendar.func())
def worker_callback_6(callback):
    result, key, step = DetailedTelegramCalendar(locale='ru').process(callback.data)
    if not result and key:
        bot.edit_message_text(
            'Введите дату',
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
        bot.set_state(callback.from_user.id, MyStates.confirm_or_fix_2, callback.message.chat.id)


@bot.callback_query_handler(state=MyStates.confirm_or_fix_2, func=lambda callback: callback.data)
def worker_callback_7(callback):
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


@bot.callback_query_handler(state=MyStates.is_photo, func=lambda callback: callback.data)
def worker_callback_8(callback):
    if callback.data == 'Да':
        bot.set_state(callback.from_user.id, MyStates.amount_photo, callback.message.chat.id)
        bot.send_message(callback.from_user.id, 'Сколько фото загрузить?')
    else:
        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            id_hostels = founding_hostels(data['dest_id'], data['amount_hostels'], data['amount_days'])

        for i_id in id_hostels[1]:
            bot.send_message(callback.from_user.id, i_id)


@bot.message_handler(state=MyStates.amount_photo)
def get_amount_photo(message: Message) -> None:
    if message.text.isdecimal():

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['amount_photo'] = int(message.text)

        id_hostels_list = founding_hostels(data['location_id'], data['amount_hostels'], data['amount_days'])

        for i_id_hostel in enumerate(id_hostels_list[0]):
            pics = founding_photo(i_id_hostel[1], data['amount_photo'])
            bot.send_media_group(
                chat_id=message.chat.id,
                media=[InputMediaPhoto(i_pic) for i_pic in pics]
            )
            bot.send_message(message.chat.id, id_hostels_list[1][i_id_hostel[0]])
            bot.set_state(message.from_user.id, None, message.chat.id)

    else:
        bot.send_message(message.chat.id, 'Введите цифрами!')

