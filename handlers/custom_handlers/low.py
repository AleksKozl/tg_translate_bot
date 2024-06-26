from datetime import datetime
from telebot.types import Message, CallbackQuery

from YaAPI.YaDictAPI import YaDict_request
from loader import bot
from states.state_translation import WordTranslate
from utils.pretty_translate_YaDict import pretty_text
from keyboards.inline.low_keyboards import low_languages_markup, low_exit_or_select_markup
import database.db_func as db_func


"""

Модуль отвечает за обработку команды 'low'.
Переводит слово полученное от пользователя по выбранному им направленю перевода.

Список функций:
    command_low - Обработчик комманды 'low'.
    welcome_to_low - Обработчик нажатия кнопок ведущих к выполнению сценария 'low'.
    language_set - Обработчик нажатия кнопок клавиатуры по выбору направления перевода.
    language_check - Проверяет наличия выбранного направления перевода среди направлений 'Яндекс.Словаря'.
    get_numbers_of_translations - Проверяет и запоминает максимальное количество вариантов перевода.
    get_word - Принимает слово для перевода.
    get_word_translate - Совершает запрос о переводе к 'Яндекс.Словарю' через модуль YaDict_request.

"""


@bot.message_handler(commands=['low'])
def command_low(message: Message) -> None:

    """
    Обработчик комманды 'low'.

    Устанавливает состояниие пользователя как 'wait'.
    Предлагает выбрать язык перевода,
    выдает клавиатуру (low_languages_markup).

    Добавляет пользователя (<class User>) в БД

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    bot.set_state(message.from_user.id, WordTranslate.wait, message.chat.id)
    db_func.db_set_state(user_id=message.from_user.id, state='wait')

    bot.send_message(
        message.from_user.id,
        text='Выберите одно из доступных направлений перевода:',
        reply_markup=low_languages_markup()
    )

    db_func.db_add_user(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        user_name=message.from_user.first_name,
        user_state='Low_Start',
        language='---'
    )


@bot.callback_query_handler(func=lambda callback: callback.data == 'low')
def welcome_to_low(callback: CallbackQuery) -> None:

    """
    Обработчик нажатия кнопок ведущих к выполнению сценария 'low'.

    Устанавливает состояниие пользователя как 'wait'.
    Редактирует предыдущее сообщение, предлагает выбрать язык перевода,
    выдает клавиатуру (low_languages_markup).

    Args:
        callback (CallbackQuery) -  Входящий запрос обратного вызова от кнопок на inline клавиатурах

    Returns:
        None
    """

    bot.set_state(callback.from_user.id, WordTranslate.wait, callback.message.chat.id)
    db_func.db_set_state(user_id=callback.from_user.id, state='wait')

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text='Выберите одно из доступных направлений перевода:',
        reply_markup=low_languages_markup()
    )


@bot.callback_query_handler(func=lambda callback: callback.data in ['ru-en', 'en-ru', 'ru-de', 'de-ru', 'all'])
def language_set(callback: CallbackQuery) -> None:

    """
    Обработчик нажатия кнопок клавиатуры (low_languages_keyboard.low_languages_markup).

    Получает результат запроса доступных языков (направлений перевода) из модуля YaDict_request.
    В случае неудачного запроса завершает работу.

    Если из предложенных кнопок выбран вариант 'Вывести все варианты' (data = 'all'):
        Высылает все доступные языки для перевода,
        предлагает выбрать из них,
        устанавливает значение атрибута user_state (str) пользователя <class User> в БД
        устанавливает состояниие пользователя как 'language'.

    Если выбран конкретный перевод из предложенных (['ru-en', 'en-ru', 'ru-de', 'de-ru']):
        Редактирует предыдущее сообщение, сигнализирует о принятии языка перевода,
        устанавливает значение атрибута user_state (str) пользователя <class User> в БД
        устанавливает значение атрибута user_selected_language (str) пользователя <class User> в БД
        устанавливает состояниие пользователя как 'word'.

    Args:
        callback (CallbackQuery) -  Входящий запрос обратного вызова от кнопок на inline клавиатурах

    Returns:
        None
    """

    langs_response = YaDict_request.langs

    if langs_response.status_code != 200:
        bot.send_message(
            callback.message.id,
            text='Не удалось получить список направлений перевода.\n'
                 'Неудачная попытка связи с "Яндекс.Словарь".\n'
                 'Повторите попытку позднее.'
        )
        exit(1)

    if callback.data == 'all':

        buf_langs = ' || '.join(YaDict_request.langs.json())

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text=buf_langs + '\n\nНапишите выбранное Вами направление как в этих примерах: ru-en, en-ru, en-de'
        )

        bot.set_state(callback.from_user.id, WordTranslate.language, callback.message.chat.id)
        db_func.db_set_state(user_id=callback.from_user.id, state='language')

    elif callback.data in ['ru-en', 'en-ru', 'ru-de', 'de-ru']:

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text=f'Принято. Ваше направление перевода: "{callback.data}"\n\n'
                 f'Введите максимальное количество вариантов перевода, которое мне нужно вывести:'
        )

        db_func.db_set_language(user_id=callback.from_user.id, language=callback.data)

        bot.set_state(callback.from_user.id, WordTranslate.numbers_of_translations, callback.message.chat.id)
        db_func.db_set_state(user_id=callback.from_user.id, state='numbers_of_translations')


@bot.message_handler(state=WordTranslate.language)
def language_check(message: Message) -> None:

    """
    Обработчик состояния пользователя, принимает состояние 'language'.
    Проверяет существует ли введенный язык (направление) перевода
    среди доступных языков (направлений перевода) из модуля YaDict_request.

    Если нет, то предлагает повторить ввод языка перевода.

    Иначе:
        редактирует предыдущее сообщение, сигнализирует о принятии языка перевода,
        предлагает написать слово для перевода,
        устанавливает значение атрибута user_state (str) пользователя <class User> в БД
        устанавливает значение атрибута user_selected_language (str) пользователя <class User> в БД
        устанавливает состояниие пользователя как 'word'.

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    if message.text not in YaDict_request.langs.json():
        bot.send_message(message.chat.id, text='Такого направления нет. Попробуйте ещё раз.')

    else:

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=f'Принято. Ваше направление перевода: "{message.text}"\n\n'
                 f'Введите максимальное количество вариантов перевода, которое мне нужно вывести:'
        )

        db_func.db_set_language(user_id=message.from_user.id, language=message.text)

        bot.set_state(message.from_user.id, WordTranslate.numbers_of_translations, message.chat.id)
        db_func.db_set_state(user_id=message.from_user.id, state='numbers_of_translations')


@bot.message_handler(state=WordTranslate.numbers_of_translations)
def get_numbers_of_translations(message: Message) -> None:

    """
    Обработчик состояния пользователя, принимает состояние 'numbers_of_translations'.
    Проверяет и запоминает максимальное количество вариантов перевода для вывода пользователю.
    Если в сообщение не целое число или оно меньше нуля, предлагает повторить ввод.

    Args:
        message (Message) - Сообщение пользователя

    Parameter:
        max_numb (int) - Максимальное количество вариантов перевода

    Returns:
        None

    Raises:
        ValueError
    """

    try:

        max_numb = int(message.text)
        if max_numb > 0:

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['numbers_of_translations'] = max_numb

                bot.send_message(
                    message.chat.id,
                    text=f'Принято, покажу максимум {max_numb} вариантов перевода.\n\n'
                         f'Теперь введите слово которое мне нужно перевести:'
                )

                bot.set_state(message.from_user.id, WordTranslate.word, message.chat.id)
                db_func.db_set_state(user_id=message.from_user.id, state='word')
        else:
            raise ValueError

    except ValueError:
        bot.send_message(
            message.chat.id,
            text='Максимальное количество переводов должно быть целым числом и больше нуля'
        )


@bot.message_handler(state=WordTranslate.word)
def get_word(message: Message) -> None:

    """
    Обработчик состояния пользователя, принимает состояние 'word'.
    Принимает слово для перевода.

    Добавляет объект слова (<class Word>) в БД.
    Выдает подтверждение принятия слова.
    Устанавливает значение атрибута user_state (str) пользователя <class User> в БД
    Устанавливает состояниие пользователя как 'word_translate'.
    Вызывает функцию get_word_translate() и передает в нее слово для перевода.

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['word'] = message.text.lower()
        db_func.db_add_word(data['word'])

    bot.send_message(message.chat.id, text=f'Принято. Перевожу: "{message.text}"')

    bot.set_state(message.from_user.id, WordTranslate.word_translate, message.chat.id)
    db_func.db_set_state(user_id=message.from_user.id, state='word_translate')

    get_word_translate(message)


@bot.message_handler(state=WordTranslate.word_translate)
def get_word_translate(message: Message) -> None:

    """
    Обработчик состояния пользователя, принимает состояние 'word_translate'.
    Совершает запрос о переводе к API 'Яндекс.Словарь' через модуль YaDict_request

    Если запрос неудачный или перевод 'пустой':
        Сообщает о неудаче и предлагает попробовать другое слово

    Иначе:
        Добавляет объект слова (<class Word>) в БД (необходимо если пользователь переводит несколько слов подряд).
        Выдает перевод через функцию pretty_text() модуля utils.pretty_translate_YaDict
        После предлагает ввести еще одно слово
        или один из вариантов команд с кнопок клавиатуры low_exit_or_select_markup()
        в которой предлагается выбор - выход в главное меню или выбор языка (повтор сценария сначала).
        А также вносит запрос типа 'low' в историю запросов.


    Parameter:
        language_selected (str) - Текущий язык (направление) перевода,
                                  атрибут user_selected_language (str) объекта <class User> из БД
        lookup_response (<class 'requests.models.Response'>) - Результат запроса о переводе

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    language_selected = db_func.db_get_language(user_id=message.from_user.id)
    lookup_response = YaDict_request.lookup(language_selected, message.text)

    if lookup_response.status_code != 200 or len(lookup_response.json()['def']) == 0:
        bot.send_message(message.chat.id, text=f'Не удалось выполнить перевод: "{message.text}"\n'
                                               f'Попробуйте другое слово.')

    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['word_translate'] = lookup_response.json()
            db_func.db_add_word(data['word'])
            target_language = db_func.db_get_language(user_id=message.from_user.id)

            data['translate_result'] = pretty_text(
                    word=data['word'],
                    language=target_language,
                    translate_json=data['word_translate'],
                    max_numbers_of_translations=data['numbers_of_translations']
                )
            if data.get('low_choice_message_id'):

                bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=data['low_choice_message_id']
                )

            bot.send_message(
                message.chat.id,
                text=data['translate_result'][0],
                )

            db_func.db_add_to_history(
                user_id=message.from_user.id,
                operation_type='low',
                operation_language=target_language,
                operation_text=data['word'],
                operation_translate=data['translate_result'][1],
                operation_datetime=f'{datetime.now()}'
            )

            low_choice_message_id = bot.send_message(
                message.chat.id,
                text='Можете написать еще одно слово или выбрать действие на кнопках.',
                reply_markup=low_exit_or_select_markup()
            ).id
            data['low_choice_message_id'] = low_choice_message_id

        bot.set_state(message.from_user.id, WordTranslate.word, message.chat.id)
        db_func.db_set_state(user_id=message.from_user.id, state='word')
