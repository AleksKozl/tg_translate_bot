from requests import post

from YaAPI.YaCloud_IAmToken.JWT_getter import jwt_request

"""
Модуль запроса IAm-токена от сервисов "Yandex.Cloud" посредством обмена JWT.
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
        print('Не удалось получить IAm-key.'
              'Следуйте инструкциям в "readme.md", чтобы его получить')
    else:
        return func_response


response = iam_key_request()
IAM_TOKEN = response.json()['iamToken']
expires_at = response.json()['expiresAt']
