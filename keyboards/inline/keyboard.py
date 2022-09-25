
# @bot.callback_query_handler(func=lambda call: True)
# def test_callback(call):
    # req_get_hostels = requests.get(
    #     url='https://hotels4.p.rapidapi.com/properties/list',
    #     params={
    #         'destinationId': call.data,
    #         'pageNumber': '1',
    #         'pageSize': '25',
    #         'adults1': '1',
    #         'sortOrder': 'PRICE',
    #         'locale': 'en_US',
    #         'currency': 'USD'
    #     },
    #     headers={
    #         'X-RapidAPI-Key': RAPID_API_KEY,
    #         'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
    #     }
    # )
    #
    #
    #
    # new_param_two = req_get_hostels.text
    # all_hostels = re.findall(r'(?<="name":")\w+\s?\w+\s?\w+\s?\w+', new_param_two)
    # hostels_id_list = re.findall(r'(?<="id":)\d{2,10}', new_param_two)
    # hostels_id_list = hostels_id_list[:len(all_hostels) + 1]
    # print(hostels_id_list)


