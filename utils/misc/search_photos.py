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

    data_hostel = json.loads(photo_hostel_req.text)
    patern = r'https://exp.cdn-hotels.com/hotels/\d+.\d+.\d+.\d+.\w+.size..{3}\w'
    finded = re.findall(patern, str(data_hostel['hotelImages'][:amount_photo]))
    pics = re.sub(r'{size}', 'l', str(finded))
    return pics

