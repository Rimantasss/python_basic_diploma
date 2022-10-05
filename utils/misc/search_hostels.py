import requests
import re
from config_data.config import RAPID_API_KEY
import json


def founding_hostels(id_location: str, amount_hostels: int, amount_days: int):
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

    pattern = r'(?<=,)"results":.+?(?=,"pagination")'
    find = re.search(pattern, hostels_req.text)
    if find:
        suggestions = json.loads(f"{{{find[0]}}}")

    id_hostels_list = list()
    info_hostel_list = list()
    for i_hostel in suggestions['results'][:amount_hostels]:
        try:
            print(i_hostel)
            id_hostels_list.append(i_hostel['id'])

            if not 'streetAddress' in i_hostel['address']:
                i_hostel['address']['streetAddress'] = 'в названии отеля'

            info_hostel = '\n🏨Отель: {}\n⭐️Рейтинг: {}\n🔑Адрес: {}\n🔍Удаленность от центра: {}\n💰Цена за сутки: {}\n💰Общая стоимость: {}'.format(
                i_hostel['name'],
                i_hostel['guestReviews']['rating'],
                i_hostel['address']['streetAddress'],
                i_hostel['landmarks'][0]['distance'],
                i_hostel['ratePlan']['price']['current'],
                '${}'.format(int(i_hostel['ratePlan']['price']['current'][1:]) * amount_days)
            )
            info_hostel_list.append(info_hostel)

        except:
            pass

    return id_hostels_list, info_hostel_list

