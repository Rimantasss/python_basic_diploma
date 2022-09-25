from loader import bot


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(
        message.from_user.id, 'Справочная информация:\n\n'
                              'Поиск по городам России на данный момент\n'
                              'временно не работает❗️❗️❗️\n'
                              'приносим свои извинения📢📢📢')
