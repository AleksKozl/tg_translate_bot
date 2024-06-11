from config_data.config import YADICT_API_KEY

import requests


BASE_URL = 'https://dictionary.yandex.net/api/v1/dicservice.json' # Обращение к .json интерфейсу API 'Яндекс.Словарь'


def get_langs() -> 'requests.models.Response':

    """
    Функция запроса доступных языков (направлений) перевода

    Parameter:
        response (<class 'requests.models.Response'>) - Результат запроса

    Returns:
        <class 'requests.models.Response'>
    """

    response = requests.get(f'{BASE_URL}/getLangs', params={
        'key': YADICT_API_KEY
    })
    return response


def lookup(lang: str, text: str, ui: str = 'ru') -> 'requests.models.Response':

    """
    Функция запроса перевода слова

    Parameter:
        response (<class 'requests.models.Response'>) - Результат запроса

    Args:
        lang (str) - Текущий язык (направление) перевода,
                     атрибут user_selected_language (str) объекта <class User> из БД
        text (str) - Слово для перевода
        ui (str) - Язык интерфейса пользователя, на котором будут отображаться названия частей речи в словарной статье

    Returns:
        <class 'requests.models.Response'>
    """

    response = requests.get(f'{BASE_URL}/lookup', params={
        'key': YADICT_API_KEY,
        'lang': lang,
        'text': text,
        'ui': ui
    })
    return response


langs = get_langs() # Результат запроса языков (направлений) перевода
