from loader import bot


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, 'Привет, {user_name}. Это телеграм бот турагенства Too Easy Travel.\n\n'
                         'Выберите интересующую вас категорию:\n'
                         '1. Помощь по командам бота /help\n'
                         '2. Узнать топ самых дешёвых отелей в городе /lowprice\n'
                         '3. Узнать топ самых дорогих отелей в городе /highprice\n'
                         '4. Узнать топ отелей, наиболее подходящих по цене и расположению от центра /bestdeal\n'
                         '5. Узнать историю поиска отелей /history\n'.format(user_name=message.chat.first_name)
    )
