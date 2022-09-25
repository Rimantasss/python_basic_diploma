import requests
import re
from config_data.config import RAPID_API_KEY


def founding_hostels(id_location: str, amount_hostels: int):
    hostels_req = requests.get(
        url='https://hotels4.p.rapidapi.com/properties/list',
        params={
            'destinationId': id_location,
            'pageNumber': '1',
            'pageSize': '25',
            'adults1': '1',
            'sortOrder': 'PRICE',
            'locale': 'ru_RU',
            'currency': 'USD'
        },
        headers={
            'X-RapidAPI-Key': RAPID_API_KEY,
            'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
        }
    )

    all_hostels = re.findall(r'(?<="name":")\w+\s?\w+\s?\w+\s?\w+', hostels_req.text)
    hostels_id_list = re.findall(r'(?<="id":)\d{2,10}', hostels_req.text)
    hostels_id_list = hostels_id_list[:amount_hostels]
    return hostels_id_list
