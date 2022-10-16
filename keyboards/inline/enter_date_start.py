from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def enter_date_start() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Ввести дату заезда', callback_data='Да'),
    )
    return markup