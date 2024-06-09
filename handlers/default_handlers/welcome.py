from telebot.types import Message

from loader import bot
from keyboards.inline.main_keyboard import main_markup
from database.db_func import db_create_tables, db_add_user


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
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
