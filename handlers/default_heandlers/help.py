from loader import bot


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(
        message.chat.id, 'Справочный информация')