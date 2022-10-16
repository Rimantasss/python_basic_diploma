from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def enter_date_finish() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Ввести дату отъезда', callback_data='Да'),
    )
    return markup