from telegram_bot_calendar import DetailedTelegramCalendar
from telebot.types import CallbackQuery
from datetime import date
from loguru import logger


@logger.catch
def create_calendar(callback_data: CallbackQuery, min_date=None, is_process=None):
    ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}

    if min_date is None:
        min_date = date.today()

    if is_process:
        try:
            result, keyboard, step = DetailedTelegramCalendar(
                locale='ru',
                min_date=min_date
            ).process(call_data=callback_data.data)
            return result, keyboard, ALL_STEPS[step]
        except KeyError:
            pass

    else:
        calendar, step = DetailedTelegramCalendar(
            locale='ru',
            current_date=min_date,
            min_date=min_date).build()
        return calendar, ALL_STEPS[step]



