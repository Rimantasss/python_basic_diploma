import requests
from config_data.config import RAPID_API_KEY
import json
from json import JSONDecodeError
from loguru import logger


@logger.catch
def founding_photo(i_hostel: str, amount_photo: int) -> list:
    """
    Функция поиска фотографий, возвращает список из ссылок на фото
    :param i_hostel: id отеля
    :param amount_photo: количество фото
    :return: list
    """
    photo_hostel_req = requests.get(
        url='https://hotels4.p.rapidapi.com/properties/get-hotel-photos',
        params={'id': i_hostel},
        headers={
            'X-RapidAPI-Key': RAPID_API_KEY,
            'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
        },
        timeout=30
    )

    list_pics = list()
    try:
        data_hostel = json.loads(photo_hostel_req.text)
        for i_image in data_hostel['hotelImages'][:amount_photo]:
            response = requests.get(i_image['baseUrl'].format(size='w'))
            if response.status_code == 200:
                list_pics.append(i_image['baseUrl'].format(size='w'))
    except JSONDecodeError:
        pass

    return list_pics

