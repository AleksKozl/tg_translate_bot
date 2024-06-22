import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
YADICT_API_KEY = os.getenv('YADICT_API_KEY')
YACLOUD_API_KEY = os.getenv('YACLOUD_API_KEY')
YACLOUD_FOLDER_ID = os.getenv('YACLOUD_FOLDER_ID')


DB_PATH = os.path.abspath(os.path.join('database', 'users_data.db'))
KEY_JSON_FILE_PATH = os.path.abspath(os.path.join('config_data', 'key.json'))
TEMP_AUDIO_PATH = os.path.abspath(os.path.join('temp', 'audio'))


DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку по командам бота. ---'),
    ('history', 'Показать историю запросов. ---'),
    ('low', 'Перевод отдельных слов.'),
    ('high', 'Перевод текстов.'),
    ('custom', 'Перевод с озвучиванием или распознавание текста на изображении')
)

