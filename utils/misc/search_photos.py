import re
import requests
from config_data.config import RAPID_API_KEY
import json


def founding_photo(i_hostel: str, amount_photo: int):
    photo_hostel_req = requests.get(
        url='https://hotels4.p.rapidapi.com/properties/get-hotel-photos',
        params={'id': i_hostel},
        headers={
            'X-RapidAPI-Key': RAPID_API_KEY,
            'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
        }
    )

    list_pics = list()
    data_hostel = json.loads(photo_hostel_req.text)
    for i_image in data_hostel['hotelImages'][:amount_photo]:
        list_pics.append(i_image['baseUrl'].format(size='w'))
    return list_pics

