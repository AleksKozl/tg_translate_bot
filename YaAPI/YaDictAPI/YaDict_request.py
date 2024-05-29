from config_data.config import YADICT_API_KEY

import requests
import pprint


BASE_URL = 'https://dictionary.yandex.net/api/v1/dicservice.json'


def get_langs():
    response = requests.get(f'{BASE_URL}/getLangs', params={
        'key': YADICT_API_KEY
    })
    return response


def lookup(lang, text, ui='ru'):
    response = requests.get(f'{BASE_URL}/lookup', params={
        'key': YADICT_API_KEY,
        'lang': lang,
        'text': text,
        'ui': ui
    })
    return response


# text = input('Введите слово или фразу для перевода: ')
# lookup_response = lookup(lang, text)
# if lookup_response.status_code != 200:
#     print('Не удалось выполнить перевод:', lookup_response.text)
#     exit(1)
#
# pprint(lookup_response.json())
