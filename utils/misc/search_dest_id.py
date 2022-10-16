import requests
import re
import json
from telebot import types
from config_data.config import RAPID_API_KEY


def city_founding(city: str):
    response = requests.get(
        url='https://hotels4.p.rapidapi.com/locations/v2/search',
        params={'query': city, 'locale': 'ru_RU', 'currency': 'USD'},
        headers={
            'X-RapidAPI-Key': RAPID_API_KEY,
            'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
        }
    )
    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, response.text)
    if find:
        suggestions = json.loads(f"{{{find[0]}}}")

        cities = list()
        for dest_id in suggestions['entities']:
            clear_destination = re.sub(
                r'</span>',
                r'',
                re.sub(r'(<span class=.highlighted.>)', r'', dest_id['caption'])
            )
            cities.append(
                {'city_name': clear_destination, 'destination_id': dest_id['destinationId']}
            )

        destinations = types.InlineKeyboardMarkup()
        for city in cities:
            destinations.add(
                types.InlineKeyboardButton(
                    text=city['city_name'], callback_data=f'{city["destination_id"]}'
                )
            )
        return destinations
