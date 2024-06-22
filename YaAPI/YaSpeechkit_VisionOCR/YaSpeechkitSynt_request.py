import requests

from config_data.config import YACLOUD_FOLDER_ID
from YaAPI.YaCloud_IAmToken.IAm_key_getter import IAM_TOKEN

"""
Модуль запросов к сервисам "Yandex.Speechkit".
"""

speechkit_url = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
speechkit_synthesis_url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'


voices_langs = ['ru', 'en', 'de']


# def audio_analyze(iam_token, folder_id, audio_data):
#     headers = {'Authorization': f'Bearer {iam_token}'}
#     params = {
#         "topic": "general",
#         "folderId": f"{folder_id}",
#         "lang": "ru-RU"}
#
#     audio_request = requests.post(
#         speechkit_url,
#         params=params,
#         headers=headers,
#         data=audio_data
#     )
#
#     response_data = audio_request.json()
#     response = 'error'
#     if response_data.get("error_code") is None:
#         response = (response_data.get("result"))
#     return response


# Синтез речи

def synthesize(text, language):

    if language == 'ru':
        language_code = 'ru-RU'
        voice_actor = 'marina'
    elif language == 'en':
        language_code = 'en-US'
        voice_actor = 'john'
    elif language == 'de':
        language_code = 'de-DE'
        voice_actor = 'lea'
    else:
        exit(1)

    headers = {
        'Authorization': 'Bearer ' + IAM_TOKEN,
    }

    data = {
        'text': text,
        'lang': language_code,
        'voice': voice_actor,
        'folderId': YACLOUD_FOLDER_ID
    }

    with requests.post(speechkit_synthesis_url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
        for chunk in resp.iter_content(chunk_size=None):
            yield chunk
