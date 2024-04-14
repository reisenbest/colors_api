import requests
from rest_framework.response import Response
from rest_framework import status


def autocomplete_title_field(hex_color: str):
    '''

    :param hex: поле hex из модели
    :return: json.file
    '''
    url = f'https://www.thecolorapi.com/id?hex={hex_color[1:]}'  # Замените на URL вашего API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        color_name = data['name']['value']

        return color_name
    else:
        return'unknown'


def unauth():
    pass
