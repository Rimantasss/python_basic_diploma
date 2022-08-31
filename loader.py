import telebot
from config_data import config
from telebot.storage import StateMemoryStorage


storage = StateMemoryStorage()
bot = telebot.TeleBot(token=config.BOT_TOKEN, state_storage=storage)
