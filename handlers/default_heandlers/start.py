from loader import bot
from telebot.types import Message
from database.data_base import create_database


@bot.message_handler(commands=['start'])
def start_message(message: Message) -> None:
    bot.send_message(
        message.from_user.id, 'Привет, {}. Это телеграм бот турагенства Too Easy Travel.\n\n'
                          'Выбор категории:\n'
                         '1. Помощь по командам бота /help\n'
                         '2. Топ самых дешёвых отелей в городе /lowprice\n'
                         '3. Топ самых дорогих отелей в городе /highprice\n'
                         '4. Топ отелей по цене и расположению от центра /bestdeal\n'
                         '5. История поиска отелей /history\n'.format(message.from_user.username)
    )

    create_database()
