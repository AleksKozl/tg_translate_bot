import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
YADICT_API_KEY = os.getenv('YADICT_API_KEY')
YATRNSLT_API_KEY = os.getenv('YATRNSLT_API_KEY')

DB_PATH = os.path.abspath(os.path.join('database', 'users_data.db'))

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку по командам бота'),
    ('history', 'Показать историю запросов'),
    ('low', 'Поиск по базам сервиса "Яндекс.Словарь"'),
    ('high', 'Поиск при помощи сервиса "Яндекс.Переводчик"'),
    ('custom', '-------Вывод всех языков?? Может выбор того, что выводить?')
)

