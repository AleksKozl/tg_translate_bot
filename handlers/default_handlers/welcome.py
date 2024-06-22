from telebot.types import Message

from loader import bot
from keyboards.inline.main_keyboards import main_markup
from database.db_func import db_create_tables, db_add_user


@bot.message_handler(commands=['start'])
def send_welcome(message: Message) -> None:

    """
    Обработчик команды "/start",
    выдает пользователю приветственное сообщение,
    клавиатуру (main_keyboard.main_markup)
    в которой представлен выбор всех доступных сценариев (help, history, low, high, custom)

    Создает таблицы всех моделей в БД,
    создает объект пользователя (<class User>)

    Parameter:
        text (str) - Приветственный текст

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    text = (
        'Привет!\n'
        'Я бот, который умеет переводить слова на другие языки.\n'
    )

    db_create_tables()
    db_add_user(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        user_name=message.from_user.first_name,
        user_state='Start',
        language='ru-en'
    )

    bot.send_message(message.from_user.id, text, reply_markup=main_markup())
