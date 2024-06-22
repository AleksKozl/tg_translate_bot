import requests

from config_data.config import YACLOUD_FOLDER_ID
from YaAPI.YaCloud_IAmToken.IAm_key_getter import IAM_TOKEN

vision_url = 'https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText'


"""
Модуль запросов к сервисам "Yandex.VisionOCR".
"""


def image_analyze(image_data):
    response = requests.post(
        vision_url,
        headers={'Authorization': 'Bearer ' + IAM_TOKEN,
                 'x-folder-id': YACLOUD_FOLDER_ID
                 },
        json={
            "mimeType": "image",
            "languageCodes": ['*'],
            "model": "page",
            "content": image_data
        }
    )

    blocks = response.json()['result']['textAnnotation']['blocks']

    text = ''

    for block in blocks:
        for line in block['lines']:
            for word in line['words']:
                text += word['text'] + ' '
            text += '\n'

    return text
