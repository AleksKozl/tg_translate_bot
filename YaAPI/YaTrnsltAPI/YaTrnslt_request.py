from requests.models import Response
from requests import post


from config_data.config import YACLOUD_API_KEY, YACLOUD_FOLDER_ID

BASE_URL = "https://translate.api.cloud.yandex.net/translate/v2"

api_token = YACLOUD_API_KEY
folder_id = YACLOUD_FOLDER_ID


def yatrnslt_translate(text: str, target_language: str,  source_language: str = None) -> Response:

    """
    Функция запроса перевода текста.

    Parameter:
        response (<class 'requests.models.Response'>) - Результат запроса

    Args:
        text (str) - Текст для перевода
        target_language (str) - Выбранный язык перевода
        source_language (str) - Язык переводимого текста


    Returns:
        <class 'requests.models.Response'>
    """

    if source_language is None:
        body = {
            "targetLanguageCode": target_language,
            "texts": text,
            "folderId": folder_id,
        }
    else:
        body = {
            "sourceLanguageCode": source_language,
            "targetLanguageCode": target_language,
            "texts": text,
            "folderId": folder_id,
        }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key {0}".format(api_token)
    }

    response = post(
        url=BASE_URL + '/translate',
        json=body,
        headers=headers
    )

    return response


def yatrnslt_get_languages() -> Response:

    """
    Функция запроса доступных языков перевода

    Parameter:
        response (<class 'requests.models.Response'>) - Результат запроса

    Returns:
        <class 'requests.models.Response'>
    """

    body = {
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key {0}".format(api_token)
    }

    response = post(
        url=BASE_URL + '/languages',
        json=body,
        headers=headers
    )

    return response


langs_request = yatrnslt_get_languages()

if langs_request.status_code == 200:
    langs_check = True
    langs_text = ''
    langs_codes = list()
    for i_lang in langs_request.json()['languages']:
        langs_text += f'Язык - "{i_lang.get('name')}"; Код языка - "{i_lang.get('code')}"\n'
        langs_codes.append(i_lang['code'])
else:
    langs_check = False
