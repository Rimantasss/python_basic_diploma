from loader import bot
from telebot.types import Message
from utils.misc.search_dest_id import city_founding
from utils.misc.search_hostels import founding_hostels
from utils.misc.search_photos import founding_photo
from states.user_states import MyStates
from config_data.config import RAPID_API_KEY
import requests
import re
import json
from telebot import types


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    bot.send_message(message.from_user.id, 'В каком городе ищем?')


@bot.message_handler(state=MyStates.city)
def city(message: Message) -> None:
    if message.text.isalpha():
        bot.set_state(message.from_user.id, MyStates.dest_id, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text

        bot.send_message(
            message.from_user.id, 'Уточните, пожалуйста:', reply_markup=city_founding(data['city'])
        )

    else:
        bot.send_message(message.chat.id, 'Назвние города должно состоять только из букв!')


@bot.callback_query_handler(state=MyStates.dest_id, func=lambda callback: callback.data)
def worker_callback(callback):
    bot.set_state(callback.from_user.id, MyStates.amount_hostels, callback.message.chat.id)
    bot.send_message(callback.message.chat.id, 'Сколько отелей показать?')

    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        data['dest_id'] = callback.data


@bot.message_handler(state=MyStates.amount_hostels)
def get_amount_hostels(message: Message) -> None:
    if message.text.isdecimal():
        bot.set_state(message.from_user.id, MyStates.is_photo, message.chat.id)
        bot.send_message(message.chat.id, 'Загрузить фото?')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['amount_hostels'] = int(message.text)

    else:
        bot.send_message(message.chat.id, 'Введите цифрами!')


@bot.message_handler(state=MyStates.is_photo)
def get_is_photo(message: Message) -> None:
    if message.text.lower() == 'да':
        if message.text.isalpha():
            bot.set_state(message.from_user.id, MyStates.amount_photo, message.chat.id)
            bot.send_message(message.from_user.id, 'Сколько фото загрузить?')

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['is_photo'] = message.text

        else:
            bot.send_message(message.chat.id, 'Введите буквами!')


@bot.message_handler(state=MyStates.amount_photo)
def get_amount_photo(message: Message) -> None:
    if message.text.isdecimal():

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['amount_photo'] = int(message.text)

        id_hostels_list = founding_hostels(data['dest_id'], data['amount_hostels'])

        for i_id_hostel in enumerate(id_hostels_list[0]):
            pics = founding_photo(i_id_hostel[1], data['amount_photo'])
            media_list = list()
            for i_pic in pics:
                media_list.append(types.InputMediaPhoto(i_pic))
            bot.send_media_group(
                chat_id=message.chat.id,
                media=media_list
            )
            bot.send_message(message.chat.id, id_hostels_list[1][i_id_hostel[0]])

    else:
        bot.send_message(message.chat.id, 'Введите цифрами!')


# print(pics)
# print(type(pics))
# bot.send_media_group(
#     chat_id=message.chat.id,
#     media=[types.InputMediaPhoto(pic) for pic in pics]

