import requests
import re
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config_data.config import RAPID_API_KEY
from loguru import logger


@logger.catch
def city_founding(city: str):
    response = requests.get(
        url='https://hotels4.p.rapidapi.com/locations/v2/search',
        params={'query': city, 'locale': 'ru_RU', 'currency': 'USD'},
        headers={
            'X-RapidAPI-Key': RAPID_API_KEY,
            'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
        },
        timeout=30
    )
    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, response.text)
    if find:
        suggestions = json.loads(f"{{{find[0]}}}")
        if len(suggestions['entities']) > 0:
            result = all_cities(suggestions)
            return result
        else:
            return None


@logger.catch
def all_cities(suggestions: dict) -> InlineKeyboardMarkup:
    cities = list()
    for dest_id in suggestions['entities']:
        clear_destination = re.sub(
            r'</span>',
            r'',
            re.sub(r'(<span class=.highlighted.>)', r'', dest_id['caption'])
        )
        cities.append({'city_name': clear_destination, 'destination_id': dest_id['destinationId']})

    destinations = InlineKeyboardMarkup()
    for city in cities:
        destinations.add(
            InlineKeyboardButton(
                text=city['city_name'], callback_data=f'{city["destination_id"]}'
            )
        )
    return destinations
