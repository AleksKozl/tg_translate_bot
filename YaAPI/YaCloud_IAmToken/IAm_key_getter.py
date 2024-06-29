import threading

from requests import post
from threading import Timer

from YaAPI.YaCloud_IAmToken.JWT_getter import jwt_request

"""
Модуль запроса IAm-токена от сервисов "Yandex.Cloud" посредством обмена JWT.

Добавлена периодичность запроса IAm-ключа, раз в 6 часов.
Реализованно с использованием отдельных потоков-таймеров.
"""

BASE_URL = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'

jwt_token = jwt_request()


def iam_key_request():

    body = {
      "jwt": jwt_token,
    }

    func_response = post(
        url=BASE_URL,
        json=body
    )

    if func_response.status_code != 200:
        print('Не удалось получить IAm-key. Код ошибки: ' + str(func_response.status_code))
    else:
        return func_response


response = iam_key_request()
IAM_TOKEN = response.json()['iamToken']
expires_at = response.json()['expiresAt']


def requesting():
    global response, IAM_TOKEN, expires_at, timer

    response = iam_key_request()
    if response:
        IAM_TOKEN = response.json()['iamToken']
        expires_at = response.json()['expiresAt']

    timer.cancel()
    timer = Timer(21600, requesting)
    timer.start()


timer = Timer(21600, requesting)
timer.start()

