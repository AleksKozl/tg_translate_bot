from telebot.types import CallbackQuery, Message

from states.state_translation import WordTranslate
from loader import bot
from keyboards.inline.main_keyboards import to_main_menu_markup
from database.db_func import db_set_state, db_add_user

help_text = (
    'Команды бота:\n'
    '\n1) /low - Перевод отдельного слова на выбранный язык (направление перевода) '
    'с выдачей определенного пользователем количества вариантов перевода.'
    '\nРезультат выводится в следующем формате:\n\n'
    '    Варианты перевода:\n'
    '        Слово_1 / (|Транскрипция|) - Перевод.\n'
    '            Синонимы:\n'
    '                Синоним_1_1 / (|Транскрипция|) - Перевод.\n'
    '                Синоним_1_2 / (|Транскрипция|) - Перевод.\n\n'
    '        Слово_2 / (|Транскрипция|) - Перевод.\n'
    '\n        .....................................\n\n'
    '        Слово_5 / (|Транскрипция|) - Перевод.\n'
    '            Синонимы:\n'
    '                Синоним_5_1 / (|Транскрипция|) - Перевод.\n\n'
    '\n2) /high - Перевод текста на выбраный язык. '
    'Имеется возможность озвучивания результата перевода. '
    '(Доступно только для Русского, Английского и Немецкого языков)\n'
    '\n3) /custom - На выбор: '
    'перевод с озвучиванием (Доступно только для Русского, Английского и Немецкого языков) '
    'или распознавание текста на изображении с последующим переводом и озвучиванием.\n'
    '\n4) /history - Выдача истории запросов.\n'
    '\n5) /help - Выдача информации по командам бота.\n'

)


@bot.callback_query_handler(func=lambda callback: callback.data == 'help')
def help_keyboard_command(callback: CallbackQuery) -> None:
    """
    "Сбрасывает" состояние пользователя и справку о возможностях бота.

    Args:
        callback (CallbackQuery) -  Входящий запрос обратного вызова от кнопок на inline клавиатурах

    Returns:
        None
    """

    bot.set_state(callback.from_user.id, WordTranslate.wait, callback.message.chat.id)
    db_set_state(user_id=callback.from_user.id, state='wait')

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=help_text,
        reply_markup=to_main_menu_markup()
    )


@bot.message_handler(commands=['help'])
def command_help(message: Message) -> None:
    """
    Обработчик комманды 'custom'.

    "Сбрасывает" состояние пользователя и справку о возможностях бота.

    Добавляет пользователя (<class User>) в БД

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    db_add_user(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        user_name=message.from_user.first_name,
        user_state='Help',
        language='---'
    )

    bot.set_state(message.from_user.id, WordTranslate.wait, message.chat.id)
    db_set_state(user_id=message.from_user.id, state='wait')

    bot.send_message(
        message.from_user.id,
        text=help_text,
        reply_markup=to_main_menu_markup()
    )
