import requests
import re
from config_data.config import RAPID_API_KEY
import json
from loguru import logger


@logger.catch
def founding_hostels(id_location: str, amount_hostels: int, amount_days: int, command: str, price_min: str = None,
                     price_max: str = None, distance_min: float = None, distance_max: float = None) -> tuple:

    if command == 'lowprice':
        param_sort = 'PRICE'
    elif command == 'highprice':
        param_sort = 'PRICE_HIGHEST_FIRST'
    else:
        param_sort = 'DISTANCE_FROM_LANDMARK'

    hostels_req = requests.get(
        url='https://hotels4.p.rapidapi.com/properties/list',
        params={
            'destinationId': id_location,
            'pageNumber': '1',
            'pageSize': '25',
            'adults1': '1',
            'priceMin': price_min,
            'priceMax': price_max,
            'sortOrder': param_sort,
            'locale': 'ru_RU',
            'currency': 'USD',
        },
        headers={
            'X-RapidAPI-Key': RAPID_API_KEY,
            'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
        },
        timeout=30
    )

    pattern = r'(?<=,)"results":.+?(?=,"pagination")'
    find = re.search(pattern, hostels_req.text)
    if find:
        suggestions = json.loads(f"{{{find[0]}}}")

        if command == 'bestdeal':
            data_hostel = sort_hotels(suggestions, distance_min, distance_max)
        else:
            data_hostel = suggestions['results']

        result = all_info(data_hostel, amount_hostels, amount_days)
        return result


@logger.catch
def sort_hotels(suggestions: dict, distance_min: float, distance_max: float) -> list:
    filter_hostel = list(filter(
        lambda x: distance_max > float(x['landmarks'][0]['distance'][:3].replace(',', '.')) > distance_min,
        suggestions['results']
    ))
    data_hostel = sorted(filter_hostel, key=lambda x: x['ratePlan']['price']['current'])
    return data_hostel


@logger.catch
def all_info(data, amount_hostels, amount_days):
    id_hostels_list, info_hostel_list, all_hostels_name = list(), list(), str()
    for i_hostel in data[:amount_hostels]:
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
            total_price = '${}'.format(
                int(i_hostel['ratePlan']['price']['current'][1:]) * amount_days
            )
        else:
            total_price = '-'

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

    return id_hostels_list, info_hostel_list, all_hostels_name
