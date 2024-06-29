from telebot.types import Message, CallbackQuery
from datetime import datetime

from YaAPI.YaTrnsltAPI import YaTrnslt_request
from loader import bot
from states.state_translation import TextTranslate
from utils.pretty_translate_YaTrnslt import pretty_text
from keyboards.inline.high_keyboards import (
    high_languages_markup,
    high_source_language_markup,
    high_exit_or_select_markup
)
import database.db_func as db_func


"""
Модуль отвечает за обработку сценария 'high'.
Переводит слово полученное от пользователя по выбранному им направлению перевода.
Также может переводить результат распознавания изображения из сценария 'custom/image'
После перевода предлагает озвучить результат при помощи сценария 'custom/voice'.

Список функций:
    command_high - Обработчик комманды 'high'.
    welcome_to_high - Обработчик нажатия кнопок ведущих к выполнению сценария 'high'.
    language_set - Обработчик нажатия кнопок клавиатуры по выбору языка перевода.
    language_check - Проверяет наличия выбранного языка перевода среди языков 'Яндекс.Переводчика'.
    source_language_choice - Обработчик нажатия кнопок ввести или нет язык переводимого текста.
    source_language_check - Проверка введенного языка переводимого текста.
    get_text - Принимает текст для перевода.
    get_text_translate - Совершает запрос о переводе к 'Яндекс.Переводчику' через модуль YaTrnslt_request.

"""


@bot.message_handler(commands=['high'])
def command_high(message: Message) -> None:

    """
    Обработчик комманды 'high'.

    Устанавливает состояниие пользователя как 'wait'.
    Предлагает выбрать язык перевод,
    выдает клавиатуру (high_languages_markup).

    Добавляет пользователя (<class User>) в БД

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    db_func.db_add_user(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        user_name=message.from_user.first_name,
        user_state='High_Start',
        language='---'
    )

    bot.set_state(message.from_user.id, TextTranslate.wait, message.chat.id)
    db_func.db_set_state(user_id=message.from_user.id, state='text_wait')

    bot.send_message(
        message.from_user.id,
        text='Выберите один из доступных языков перевода:',
        reply_markup=high_languages_markup()
    )


@bot.callback_query_handler(func=lambda callback: callback.data in ['high', 'image_to_high'])
def welcome_to_high(callback: CallbackQuery):

    """
    Обработчик нажатия кнопок ведущих к выполнению сценария 'high'.

    Устанавливает состояниие пользователя как 'wait'.
    Редактирует предыдущее сообщение, предлагает выбрать язык перевода,
    для этого выдает клавиатуру (high_languages_markup).

    В случае перевода распознанного на изображении текста - поднимает соответствующий флаг.

    Args:
        callback (CallbackQuery) -  Входящий запрос обратного вызова от кнопок на inline клавиатурах

    Returns:
        None
    """

    bot.set_state(callback.from_user.id, TextTranslate.wait, callback.message.chat.id)
    db_func.db_set_state(user_id=callback.from_user.id, state='text_wait')

    if callback.data == 'image_to_high':
        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data['image_to_high_flag'] = True

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text='Выберите один из доступных языков перевода:',
        reply_markup=high_languages_markup()
    )


@bot.callback_query_handler(func=lambda callback: callback.data in ['ru', 'en', 'de', 'fr', 'all'])
def language_set(callback: CallbackQuery) -> None:

    """
    Обработчик нажатия кнопок клавиатуры (high_languages_keyboard.high_languages_markup).

    Получает результат запроса доступных языков из модуля YaTrnslt_request.
    В случае неудачного запроса завершает работу.

    Если из предложенных кнопок выбран вариант 'Вывести все варианты' (data = 'all'):
        Высылает все доступные языки для перевода,
        предлагает выбрать из них,
        устанавливает значение атрибута user_state (str) пользователя <class User> в БД
        устанавливает состояниие пользователя как 'target_language'.

    Если выбран конкретный перевод из предложенных (['ru', 'en', 'de', 'fr']):
        Редактирует предыдущее сообщение, сигнализирует о принятии языка перевода,
        устанавливает значение атрибута user_state (str) пользователя <class User> в БД
        устанавливает значение атрибута user_selected_language (str) пользователя <class User> в БД
        устанавливает состояниие пользователя как 'source_language'.
        При помощи клавиатуры high_source_language_markup
        предлагает выбрать вводить или нет язык переводимого текста.

        В случае если переводится распознанный на изображении текст - переходит к переводу.

    Parameter:
        image_to_high_flag (bool) - Флаг перехода от сценария "custom/image"

    Args:
        callback (CallbackQuery) -  Входящий запрос обратного вызова от кнопок на inline клавиатурах

    Returns:
        None
    """

    if not YaTrnslt_request.langs_check:
        bot.send_message(
            callback.message.chat.id,
            text='Не удалось получить список языков перевода.\n'
                 'Неудачная попытка связи с "Яндекс.Переводчик".\n'
                 'Повторите попытку позднее.'
        )
        exit(1)

    if callback.data == 'all':

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text=YaTrnslt_request.langs_text + '\n\nНапишите код выбранного Вами языка как в этих примерах: ru, en, de'
        )

        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data['message_id_with_all_langs'] = callback.message.id

        bot.set_state(callback.from_user.id, TextTranslate.target_language, callback.message.chat.id)
        db_func.db_set_state(user_id=callback.from_user.id, state='text_language')

    elif callback.data in ['ru', 'en', 'de', 'fr']:

        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            image_to_high_flag = data.get('image_to_high_flag')
            data['target_language'] = callback.data
            db_func.db_set_language(user_id=callback.from_user.id, language=callback.data)

        if image_to_high_flag:
            bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.id,
                text=f'Принято. Ваш язык перевода: "{callback.data}"'
            )

            get_text(message=callback.message)

        else:
            bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.id,
                text=f'Принято. Ваш язык перевода: "{callback.data}"\n'
                     f'Желаете выбрать язык переводимого текста?:',
                reply_markup=high_source_language_markup()
            )

            bot.set_state(callback.from_user.id, TextTranslate.source_language, callback.message.chat.id)
            db_func.db_set_state(user_id=callback.from_user.id, state='text_source_language')


@bot.message_handler(state=TextTranslate.target_language)
def language_check(message: Message) -> None:

    """
    Обработчик состояния пользователя, принимает состояние 'target_language'.
    Проверяет существует ли введенный язык перевода
    среди доступных языков из модуля YaTrnslt_request.

    Если нет, то предлагает повторить ввод языка перевода.

    Иначе:
        редактирует предыдущее сообщение, сигнализирует о принятии языка перевода,
        предлагает написать слово для перевода,
        устанавливает значение атрибута user_state (str) пользователя <class User> в БД
        устанавливает значение атрибута user_selected_language (str) пользователя <class User> в БД
        устанавливает состояниие пользователя как 'text_source_language'.
        При помощи клавиатуры high_source_language_markup
        предлагает выбрать вводить или нет язык переводимого текста.

        В случае если переводится распознанный на изображении текст - переходит к переводу.


    Parameter:
        image_to_high_flag (bool) - Флаг перехода от сценария "custom/image"

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    if message.text not in YaTrnslt_request.langs_codes:
        bot.send_message(message.chat.id, text='Такого языка нет в списке. Попробуйте ещё раз.')

    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            all_langs_message_id = data['message_id_with_all_langs']
            image_to_high_flag = data['image_to_high_flag']

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=all_langs_message_id,
            text=f'Список всех языков скрыт.'
        )

        if image_to_high_flag:
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Принято. Ваш язык перевода: "{message.text}"\n'
            )
            get_text(message)

        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Принято. Ваш язык перевода: "{message.text}"\n'
                     f'Желаете выбрать язык переводимого текста?:',
                reply_markup=high_source_language_markup()
            )

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['target_language'] = message.text
            db_func.db_set_language(user_id=message.from_user.id, language=message.text)

        bot.set_state(message.from_user.id, TextTranslate.source_language, message.chat.id)
        db_func.db_set_state(user_id=message.from_user.id, state='text_source_language')


@bot.callback_query_handler(func=lambda callback: callback.data in ['source_language_yes', 'source_language_no'])
def source_language_choice(callback: CallbackQuery) -> None:

    """
    Обработчик нажатия кнопок клавиатуры high_source_language_markup.

    Получает результат запроса доступных языков из модуля YaTrnslt_request.
    В случае неудачного запроса завершает работу.

    Если из предложенных кнопок 'Да' (data = 'source_language_yes'):
        Редактирует предыдущее сообщение,
        устанавливает значение атрибута user_state (str) пользователя <class User> в БД
        устанавливает состояниие пользователя как 'source_language'.
        Предлагает ввести код языка с которого нужно переводить.


    Если из предложенных кнопок 'Нет' (data = 'source_language_no'):
        Запоминает в памяти бота значение source_language.
        Редактирует предыдущее сообщение, предлагает ввести текст для перевода,
        устанавливает значение атрибута user_state (str) пользователя <class User> в БД
        устанавливает состояниие пользователя как 'text'.

    Args:
        callback (CallbackQuery) -  Входящий запрос обратного вызова от кнопок на inline клавиатурах

    Returns:
        None
    """

    if callback.data == 'source_language_yes':

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='Введите язык, с которого нужно будет переводить:\n'
                 'Напишите код выбранного Вами языка как в этих примерах: ru, en, de'
        )

        bot.set_state(callback.from_user.id, TextTranslate.source_language, callback.message.chat.id)
        db_func.db_set_state(user_id=callback.from_user.id, state='text_source_language')

    elif callback.data == 'source_language_no':

        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data['source_language'] = None

            bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.id,
                text='Теперь введите текст который мне нужно перевести:'
            )

            bot.set_state(callback.from_user.id, TextTranslate.text, callback.message.chat.id)
            db_func.db_set_state(user_id=callback.from_user.id, state='text_text')


@bot.message_handler(state=TextTranslate.source_language)
def source_language_check(message: Message) -> None:

    """
    Обработчик состояния пользователя, принимает состояние 'source_language'.
    Проверяет и запоминает значение языка переводимого текста (source_language).
    Если такого языка в списке YaTrnslt_request.langs_codes нет, предлагает повторить ввод.
    Устанавливает значение атрибута user_state (str) пользователя <class User> в БД
    устанавливает состояниие пользователя как 'text'.

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    if message.text not in YaTrnslt_request.langs_codes:
        bot.send_message(message.chat.id, text='Такого языка нет в списке. Попробуйте ещё раз.')

    else:

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['source_language'] = message.text

        bot.send_message(
            message.chat.id,
            text=f'Принято, язык Вашего текста будет "{message.text}".\n\n'
                 f'Теперь введите текст который мне нужно перевести:'
        )

        bot.set_state(message.from_user.id, TextTranslate.text, message.chat.id)
        db_func.db_set_state(user_id=message.from_user.id, state='text_text')


@bot.message_handler(state=TextTranslate.text)
def get_text(message: Message) -> None:

    """
    Обработчик состояния пользователя, принимает состояние 'text'.
    Принимает текст для перевода.
    В случае если переводится распознанный на изображении текст - берет текст из истории запросов.

    Выдает подтверждение принятия текста.
    Устанавливает значение атрибута user_state (str) пользователя <class User> в БД
    Устанавливает состояниие пользователя как 'text_translate'.
    Вызывает функцию get_text_translate() и передает в нее текст для перевода.

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    with bot.retrieve_data(message.chat.id) as data:

        if data.get('image_to_high_flag'):
            latest_translate = db_func.db_get_history(user_id=message.chat.id)[-1]
            data['text'] = latest_translate.operation_text
        else:
            data['text'] = message.text

    bot.send_message(message.chat.id, text=f'Принято. Перевожу Ваш текст.')

    bot.set_state(message.chat.id, TextTranslate.text_translate, message.chat.id)
    db_func.db_set_state(user_id=message.chat.id, state='text_text_translate')

    get_text_translate(message)


@bot.message_handler(state=TextTranslate.text_translate)
def get_text_translate(message: Message) -> None:

    """
    Обработчик состояния пользователя, принимает состояние 'text_translate'.
    Совершает запрос о переводе к API 'Яндекс.Переводчик' через модуль YaTrnslt_request

    Если запрос неудачный:
        Сообщает о неудаче и предлагает попробовать другой текст

    Иначе:
        Выдает перевод через функцию pretty_text() модуля utils.pretty_translate_YaTrnslt
        После предлагает ввести еще одно слово
        или один из вариантов команд с кнопок клавиатуры high_exit_or_select_markup
        в которой предлагается выбор - выход в главное меню или выбор языка (повтор сценария сначала).
        А также вносит запрос типа 'high' в историю запросов.

    Опускает флаг перевода распознанного на изображении текста.


    Parameter:
        source_language (str) - Язык переводимого текста
        target_language (str) - Текущий язык перевода
        lookup_response (<class 'requests.models.Response'>) - Результат запроса о переводе
        pretty_translation (str) - Приведенный к нужному для вывода пользователю виду результат перевода

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    with bot.retrieve_data(message.chat.id) as data:
        source_language = data.get('source_language')
        target_language = data.get('target_language')
        data['image_to_high_flag'] = False
        target_text = data.get('text')

    lookup_response = YaTrnslt_request.yatrnslt_translate(
        text=target_text,
        target_language=target_language,
        source_language=source_language
    )

    if lookup_response.status_code != 200:
        bot.send_message(message.chat.id, text=f'Не удалось выполнить перевод.\n'
                                               f'Попробуйте другой текст.')

    else:

        pretty_translation = pretty_text(
                translate_json=lookup_response.json(),
                text_for_translation=target_text
            )

        with bot.retrieve_data(message.chat.id) as data:
            if data.get('high_choice_message_id'):

                bot.edit_message_reply_markup(
                    message_id=data.get('high_choice_message_id'),
                    chat_id=message.chat.id,
                    reply_markup=None
                )

            high_choice_message_id = bot.send_message(
                message.chat.id,
                text=pretty_translation[0] + '\n\nМожете написать еще текст или выбрать действие на кнопках.',
                reply_markup=high_exit_or_select_markup(),
            ).id
            data['high_choice_message_id'] = high_choice_message_id

        db_func.db_add_to_history(
            user_id=message.chat.id,
            operation_type='high',
            operation_language=target_language,
            operation_text=target_text,
            operation_translate=pretty_translation[1],
            operation_datetime=f'{datetime.now()}'
        )

    bot.set_state(message.chat.id, TextTranslate.text, message.chat.id)
    db_func.db_set_state(user_id=message.chat.id, state='text_text')
