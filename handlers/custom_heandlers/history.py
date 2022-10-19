from loader import bot
from telebot.types import Message, CallbackQuery
from keyboards.inline.confirm_buttons import confirm
from states.user_states import MyStates
from telegram_bot_calendar import DetailedTelegramCalendar
from database.get_from_db import get_from_db


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    bot.set_state(message.from_user.id, MyStates.date_start_1, message.chat.id)
    bot.send_message(
        message.from_user.id,
        'Поиск истории по датам',
        reply_markup=confirm()
    )


@bot.callback_query_handler(state=MyStates.date_start_1, func=None)
def enter_date(callback: CallbackQuery) -> None:
    if callback.data == 'Да':
        ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}
        bot.set_state(callback.from_user.id, MyStates.date_start_2, callback.message.chat.id)
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
        calendar, step = DetailedTelegramCalendar(locale='ru').build()
        bot.send_message(callback.message.chat.id, 'Введите {}'.format(ALL_STEPS[step]), reply_markup=calendar)


@bot.callback_query_handler(state=MyStates.date_start_2, func=None)
def enter_date_next(callback: CallbackQuery) -> None:
    ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}
    result, key, step = result, keyboard, step = DetailedTelegramCalendar(locale='ru').process(call_data=callback.data)
    if not result and key:
        bot.edit_message_text(
            'Введите {}'.format(ALL_STEPS[step]),
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=key
        )
    elif result:
        bot.edit_message_text(
            'Дата начала поиска истории: {}'.format(result),
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=confirm()
        )
        bot.set_state(callback.from_user.id, MyStates.date_end_1, callback.message.chat.id)

        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data['date_start_1'] = result


@bot.callback_query_handler(state=MyStates.date_end_1, func=None)
def enter_date(callback: CallbackQuery) -> None:
    if callback.data == 'Да':
        ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}
        bot.set_state(callback.from_user.id, MyStates.date_end_2, callback.message.chat.id)
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
        calendar, step = DetailedTelegramCalendar(locale='ru').build()
        bot.send_message(callback.message.chat.id, 'Введите {}'.format(ALL_STEPS[step]), reply_markup=calendar)


@bot.callback_query_handler(state=MyStates.date_end_2, func=None)
def enter_date_next(callback: CallbackQuery) -> None:
    ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}
    result, key, step = result, keyboard, step = DetailedTelegramCalendar(locale='ru').process(call_data=callback.data)
    if not result and key:
        bot.edit_message_text(
            'Введите {}'.format(ALL_STEPS[step]),
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=key
        )
    elif result:
        bot.edit_message_text(
            'Дата конца поиска истории: {}'.format(result),
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=confirm()
        )
        bot.set_state(callback.from_user.id, MyStates.search_history, callback.message.chat.id)

        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data['date_end_1'] = result


@bot.callback_query_handler(state=MyStates.search_history, func=None)
def search_history(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)

    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        date_start = data['date_start_1']
        date_finish = data['date_end_1']

    history = get_from_db(date_start, date_finish)

    if history:
        for i in history:
            command, date, time, hostels = i
            i_history = 'Команда:  {command}\n\nДата:  {date}\n\nВремя:  {time}\n\nОтели:  {hostels}\n'.format(
                command=command, date=date, time=time, hostels=hostels
            )
            bot.send_message(callback.message.chat.id, i_history)
        bot.set_state(callback.from_user.id, None, callback.message.chat.id)
    else:
        bot.send_message(callback.message.chat.id, 'За выбранный период времени нет историй')
        bot.set_state(callback.from_user.id, None, callback.message.chat.id)
