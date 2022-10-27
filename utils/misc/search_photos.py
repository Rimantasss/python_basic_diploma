import requests
from config_data.config import RAPID_API_KEY
import json
from json import JSONDecodeError
from loguru import logger


def founding_photo(i_hostel: str, amount_photo: int) -> list:
    photo_hostel_req = requests.get(
        url='https://hotels4.p.rapidapi.com/properties/get-hotel-photos',
        params={'id': i_hostel},
        headers={
            'X-RapidAPI-Key': RAPID_API_KEY,
            'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
        }
    )

    list_pics = list()
    print(photo_hostel_req.status_code, photo_hostel_req.text)
    try:
        data_hostel = json.loads(photo_hostel_req.text)
        for i_image in data_hostel['hotelImages'][:amount_photo]:
            response = requests.get(i_image['baseUrl'].format(size='w'))
            if response.status_code == 200:
                list_pics.append(i_image['baseUrl'].format(size='w'))

    except (JSONDecodeError, TypeError) as exc:
        logger.exception(exc)

    return list_pics

