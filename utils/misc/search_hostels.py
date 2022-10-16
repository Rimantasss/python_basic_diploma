import requests
import re
from config_data.config import RAPID_API_KEY
import json


def founding_hostels(id_location: str, amount_hostels: int, amount_days: int) -> tuple:
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
    all_hostels_name = str()
    for i_hostel in suggestions['results'][:amount_hostels]:
        name = i_hostel.get('name', '-')
        all_hostels_name += ''.join('{}\n'.format(name))

        if 'guestReviews' in i_hostel:
            rating = i_hostel['guestReviews'].get('rating', '-')
        else:
            rating = '-'

        if 'address' in i_hostel:
            adress = i_hostel['address'].get('streetAddress', '-')
        else:
            adress = '-'

        if 'landmarks' in i_hostel:
            distance = i_hostel['landmarks'][0].get('distance', '-')
        else:
            distance = '-'

        if 'ratePlan' in i_hostel:
            if 'price' in i_hostel['ratePlan']:
                price = i_hostel['ratePlan']['price'].get('current', '-')
            else:
                price = '-'
        else:
            price = '-'

        if price != '-':
            total_price = '${}'.format(int(i_hostel['ratePlan']['price']['current'][1:]) * amount_days)
        else:
            total_price = '-'

        try:
            id_hostels_list.append(i_hostel['id'])
            link = 'https://hotels.com/ho{}'.format(i_hostel['id'])
            info_hostel = '\n🏨Отель: {}' \
                          '\n⭐️Рейтинг: {}' \
                          '\n🔑Адрес: {}' \
                          '\n🔍Удаленность от центра: {}' \
                          '\n💵Цена за сутки: {}' \
                          '\n💰Общая стоимость: {}' \
                          '\n💾Ссылка на отель: {}'.format(name, rating, adress, distance, price, total_price, link)
            info_hostel_list.append(info_hostel)
        except:
            pass

    return id_hostels_list, info_hostel_list, all_hostels_name
