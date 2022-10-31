from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def amount_photo() -> InlineKeyboardMarkup:
    """Функция создает клавиатуру из кнопок с цифрами от 1 до 9"""
    markup = InlineKeyboardMarkup(row_width=3)
    item_1 = InlineKeyboardButton(text='1', callback_data=1)
    item_2 = InlineKeyboardButton(text='2', callback_data=2)
    item_3 = InlineKeyboardButton(text='3', callback_data=3)
    item_4 = InlineKeyboardButton(text='4', callback_data=4)
    item_5 = InlineKeyboardButton(text='5', callback_data=5)
    item_6 = InlineKeyboardButton(text='6', callback_data=6)
    item_7 = InlineKeyboardButton(text='7', callback_data=7)
    item_8 = InlineKeyboardButton(text='8', callback_data=8)
    item_9 = InlineKeyboardButton(text='9', callback_data=9)
    markup.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7, item_8, item_9)
    return markup


def confirm() -> InlineKeyboardMarkup:
    """Функция создает клавиатуру с кнопкой подтвердить действие"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Подтвердить', callback_data='Да'))
    return markup


def enter_date_start() -> InlineKeyboardMarkup:
    """Функция создает клавиатуру с кнопкой ввести дату заезда"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Ввести дату заезда', callback_data='Да'))
    return markup


def enter_date_finish() -> InlineKeyboardMarkup:
    """Функция создает клавиатуру с кнопкой ввести дату отъезда"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Ввести дату отъезда', callback_data='Да'))
    return markup


def yes_or_no() -> InlineKeyboardMarkup:
    """Функция создает клавиатуру с кнопками да/нет"""
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Да', callback_data='Да'),
        InlineKeyboardButton(text='Нет', callback_data='Нет')
    )
    return markup


def link_button(link: str) -> InlineKeyboardMarkup:
    """Функция создает клавиатуру с кнопкой ссылкой на отель"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Ссылка на отель', url=link))
    return markup