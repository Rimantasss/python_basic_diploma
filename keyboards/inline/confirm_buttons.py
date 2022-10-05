from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Подтвердить', callback_data='Да'),
    )
    return markup
