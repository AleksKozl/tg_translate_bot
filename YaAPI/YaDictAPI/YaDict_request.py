from config_data.config import YADICT_API_KEY

import requests


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


langs = get_langs()
