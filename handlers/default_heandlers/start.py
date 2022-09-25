from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['start'])
def start_message(message: Message) -> None:
    bot.send_message(
        message.from_user.id, 'Привет, {}. Это телеграм бот турагенства Too Easy Travel.\n\n'
                         'Выберите интересующую вас категорию:\n'
                         '1. Получить дополнительную информацию /help\n'
                         '2. Узнать топ самых дешёвых отелей в городе /lowprice\n'
                         '3. Узнать топ самых дорогих отелей в городе /highprice\n'
                         '4. Узнать топ отелей, наиболее подходящих по цене и расположению от центра /bestdeal\n'
                         '5. Узнать историю поиска отелей /history\n'.format(message.from_user.username)
    )
