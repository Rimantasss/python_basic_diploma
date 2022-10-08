from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def enter_date():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Ввести дату', callback_data='Да'),
    )
    return markup