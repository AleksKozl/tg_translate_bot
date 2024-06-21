import time
import jwt
import json

from config_data.config import KEY_JSON_FILE_PATH

"""
Модуль создания JWT для последующего обмена на IAm-токен.
"""

try:
    with open(KEY_JSON_FILE_PATH, 'r') as key_json_file:
        obj = key_json_file.read()
        obj = json.loads(obj)
        private_key = obj['private_key']
        key_id = obj['id']
        service_account_id = obj['service_account_id']

except FileNotFoundError:
    exit('В директории "config_data" отстутствует файл "key.json". '
         'Следуйте инструкциям в "readme.md", чтобы его получить')


def jwt_request():
    now = int(time.time())
    payload = {
        'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
        'iss': service_account_id,
        'iat': now,
        'exp': now + 3600
    }

    # Формирование JWT.
    encoded_token = jwt.encode(
        payload,
        private_key,
        algorithm='PS256',
        headers={'kid': key_id}
    )

    return encoded_token
