from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Подтвердить', callback_data='Да'),
    )
    return markup
