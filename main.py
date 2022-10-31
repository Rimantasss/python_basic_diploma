from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from loguru import logger


if __name__ == '__main__':
    logger.add('logs.log', format='{time} {level} {message}', level='DEBUG')
    try:
        bot.add_custom_filter(StateFilter(bot))
        set_default_commands(bot)
        bot.infinity_polling()
    except Exception as exc:
        logger.exception(exc)



