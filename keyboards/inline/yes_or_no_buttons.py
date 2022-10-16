from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_or_no() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Да', callback_data='Да'),
        InlineKeyboardButton(text='Нет', callback_data='Нет')
    )
    return markup
