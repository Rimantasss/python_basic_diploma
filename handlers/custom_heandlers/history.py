from loader import bot
from telebot.types import Message, CallbackQuery
from keyboards.inline.keyboard import confirm
from keyboards.inline.calendar import all_steps
from states.user_states import MyStates
from telegram_bot_calendar import DetailedTelegramCalendar
from database.data_base import get_from_db


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    bot.set_state(chat_id=message.from_user.id, state=MyStates.date_start_1, user_id=message.chat.id)
    bot.send_message(chat_id=message.from_user.id, text='Поиск истории по датам', reply_markup=confirm())


@bot.callback_query_handler(state=MyStates.date_start_1, func=None)
def enter_date_start(callback: CallbackQuery) -> None:
    bot.set_state(chat_id=callback.from_user.id, state=MyStates.date_start_2, user_id=callback.message.chat.id)
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    bot.send_message(chat_id=callback.from_user.id, text='Введите {}'.format(all_steps()[step]), reply_markup=calendar)


@bot.callback_query_handler(state=MyStates.date_start_2, func=None)
def enter_date_next(callback: CallbackQuery) -> None:
    result, key, step = result, keyboard, step = DetailedTelegramCalendar(locale='ru').process(call_data=callback.data)
    if not result and key:
        bot.edit_message_text(
            text='Введите {}'.format(all_steps()[step]),
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=key
        )
    elif result:
        bot.edit_message_text(
            text='Дата начала поиска истории: {}'.format(result),
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=confirm()
        )
        bot.set_state(chat_id=callback.from_user.id, state=MyStates.date_end_1, user_id=callback.message.chat.id)

        with bot.retrieve_data(chat_id=callback.from_user.id, user_id=callback.message.chat.id) as data:
            data['date_start_1'] = result


@bot.callback_query_handler(state=MyStates.date_end_1, func=None)
def enter_date_finish(callback: CallbackQuery) -> None:
    bot.set_state(chat_id=callback.from_user.id, state=MyStates.date_end_2, user_id=callback.message.chat.id)
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    bot.send_message(chat_id=callback.from_user.id, text='Введите {}'.format(all_steps()[step]), reply_markup=calendar)


@bot.callback_query_handler(state=MyStates.date_end_2, func=None)
def enter_date_next(callback: CallbackQuery) -> None:
    result, key, step = result, keyboard, step = DetailedTelegramCalendar(locale='ru').process(call_data=callback.data)
    if not result and key:
        bot.edit_message_text(
            text='Введите {}'.format(all_steps()[step]),
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=key
        )
    elif result:
        bot.edit_message_text(
            text='Дата конца поиска истории: {}'.format(result),
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=confirm()
        )
        bot.set_state(chat_id=callback.from_user.id, state=MyStates.search_history, user_id=callback.message.chat.id)

        with bot.retrieve_data(chat_id=callback.from_user.id, user_id=callback.message.chat.id) as data:
            data['date_end_1'] = result


@bot.callback_query_handler(state=MyStates.search_history, func=None)
def search_history(callback: CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id)

    with bot.retrieve_data(chat_id=callback.from_user.id, user_id=callback.message.chat.id) as data:
        date_start = data['date_start_1']
        date_finish = data['date_end_1']

    my_history = get_from_db(date_start, date_finish)

    if my_history:
        for i in my_history:
            command, date, time, hostels = i
            i_history = 'Команда:  {command}\n\n' \
                        'Дата:  {date}\n\n' \
                        'Время:  {time}\n\n' \
                        'Отели:  {hostels}\n'.format(
                            command=command, date=date, time=time, hostels=hostels
                        )
            bot.send_message(chat_id=callback.from_user.id, text=i_history)
        bot.set_state(chat_id=callback.from_user.id, state=None, user_id=callback.message.chat.id)
    else:
        bot.send_animation(
            chat_id=callback.from_user.id,
            animation='https://i.gifer.com/7VE.gif',
            caption='За выбранный период времени нет историй'
        )
        bot.set_state(chat_id=callback.from_user.id, state=None, user_id=callback.message.chat.id)
