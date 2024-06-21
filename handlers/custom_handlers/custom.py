from datetime import datetime
from os import remove, sep
from telebot.types import Message, CallbackQuery

from YaAPI.YaSpeechkit_VisionOCR.YaSpeechkitSynt_request import synthesize
from YaAPI.YaTrnsltAPI.YaTrnslt_request import yatrnslt_translate
from loader import bot
from states.state_translation import VoiceSynt
from utils.pretty_translate_YaTrnslt import pretty_text
from keyboards.inline.custom_keyboards import (
    custom_main_markup,
    custom_languages_markup,
    custom_high_to_voice_markup,
    custom_exit_or_select_markup
)
from database import db_func
from config_data.config import TEMP_AUDIO_PATH

"""
Модуль отвечает за обработку команды 'custom'.
Содержит два подсценария: 'image' и 'voice'.

    Подсценарий 'image':
    
        *Pass*
    
    Подсценарий 'voice':
        Переводит и озвучивает введенный пользователем текст. 
        Может быть использован как дополнение к сценарию 'high'. 
        В таком случае озвучивает последний переведенный для пользователя текст.


Список функций:
    welcome_to_custom - Обработчик нажатия кнопок ведущих к выполнению сценария 'custom'.
    high_to_voice - Осуществляет озвучивание текста переведенного в сценарии 'high' (последнего в истории запросов).
    custom_to_image_main - Запускает сценарий определения текста на изображении.
    
    custom_to_voice_main - Запускает подсценарий перевода и озвучивания, предлагает выбрать язык из 3 возможных.
    voice_main_to_text - Обрабатывает выбранный язык, предлагает ввести текст.
    voice_text - Принимает текст для перевода.
    voice_text_translation - Совершает запрос о переводе к 'Яндекс.Переводчику' через модуль YaTrnslt_request.
    voice_voice_synthesize - Совершает запрос о синтезе озвучивания к 'Yandex.Speechkit' 
                             через модуль YaSpeechkitSynt_request

"""


@bot.callback_query_handler(func=lambda callback: callback.data == 'custom')
def welcome_to_custom(callback: CallbackQuery) -> None:

    """
    Обработчик нажатия кнопок ведущих к выполнению сценария 'custom'.

    Устанавливает состояниие пользователя как 'wait'.
    Редактирует предыдущее сообщение, предлагает выбрать подсценарий,
    выдает клавиатуру (custom_main_markup()).

    Args:
        callback (CallbackQuery) -  Входящий запрос обратного вызова от кнопок на inline клавиатурах

    Returns:
        None
    """

    bot.set_state(callback.from_user.id, VoiceSynt.wait, callback.message.chat.id)
    db_func.db_set_state(user_id=callback.from_user.id, state='voice_wait')

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=f'Выберете желаемое действие на клавиатуре ниже.',
        reply_markup=custom_main_markup()
    )


@bot.callback_query_handler(func=lambda callback: callback.data in ['high_to_voice'])
def high_to_voice(callback: CallbackQuery) -> None:

    """
    Осуществляет озвучивание текста переведенного в сценарии 'high' (последнего в истории запросов).

    Проверяет использованный для перевода язык.

    Если язык не поддерживается для озвучивания:
        выдает клавиатуру custom_high_to_voice_markup
        с выбором "Выход в главное меню" и "Выбрать язык" (запуск подсценария 'voice')
    Иначе:
        Запрашивает из БД последний перевод и передает его и язык в voice_voice_synthesize для озвучивания.
        А также вносит запрос типа 'high_to_voice' в историю запросов.

    Args:
        callback (CallbackQuery) -  Входящий запрос обратного вызова от кнопок на inline клавиатурах

    Returns:
        None
    """

    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:

        data['source_language'] = None

        if data['target_language'] not in ['ru', 'en', 'de']:

            bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.id,
                text=f'Озвучить возможно только тексты на Русском, Английском и Немецком языках.'
                     f'Желаете продолжить?',
                reply_markup=custom_high_to_voice_markup()
            )

        else:
            data['voice_target_language'] = data['target_language']
            latest_translate = db_func.db_get_history(user_id=callback.from_user.id)[-1]

            bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.id,
                text='Произвожу озвучивание перевода Вашего текста.\n'
                     f'\n\nПеревод - {latest_translate.operation_translate}; '
                     f'\n\nЯзык - {data['voice_target_language']};'
            )

            db_func.db_add_to_history(
                user_id=callback.from_user.id,
                operation_type='high_to_voice',
                operation_language=data['voice_target_language'],
                operation_text=latest_translate.operation_text,
                operation_translate=latest_translate.operation_translate,
                operation_datetime=f'{datetime.now()}'
            )

            voice_voice_synthesize(
                user_id=callback.from_user.id,
                voice_translate=latest_translate.operation_translate,
                voice_language=data['voice_target_language']
            )


@bot.callback_query_handler(func=lambda callback: callback.data == 'image')
def custom_to_image_main(callback: CallbackQuery) -> None:
    pass


@bot.callback_query_handler(func=lambda callback: callback.data == 'voice')
def custom_to_voice_main(callback: CallbackQuery) -> None:

    """
    Запускает подсценарий перевода и озвучивания,
    предлагает выбрать на клавиатуре custom_languages_markup() язык из 3 возможных.

    Устанавливает значение атрибута user_state (str) пользователя <class User> в БД
    Устанавливает состояниие пользователя как 'target_language'.


    Args:
        callback (CallbackQuery) -  Входящий запрос обратного вызова от кнопок на inline клавиатурах

    Returns:
        None
    """

    bot.set_state(callback.from_user.id, VoiceSynt.target_language, callback.message.chat.id)
    db_func.db_set_state(user_id=callback.from_user.id, state='voice_language')

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=f'Я могу озвучить текст только на трёх языках.\n'
             f'Они указанны на кнопках, пожалуйста выберете нужный Вам.\n\n',
        reply_markup=custom_languages_markup()
    )


@bot.callback_query_handler(func=lambda callback: callback.data in ['voice_ru', 'voice_en', 'voice_de'])
def voice_main_to_text(callback: CallbackQuery) -> None:

    """
    Обрабатывает выбранный язык, предлагает ввести текст для перевода и озвучивания

    Устанавливает значение атрибута user_state (str) пользователя <class User> в БД
    Устанавливает состояниие пользователя как 'text_for_voice'.

    Parameter:
        target_language (str) - Выбранный для перевода язык

    Args:
        callback (CallbackQuery) -  Входящий запрос обратного вызова от кнопок на inline клавиатурах

    Returns:
        None
    """

    target_language = callback.data.split('_')[1]

    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        data['voice_target_language'] = target_language

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=f'Принято. Ваш язык перевода: "{target_language}"\n\n'
             f'Теперь введите слово или текст для перевода с озвучкой результата.'
    )

    bot.set_state(callback.from_user.id, VoiceSynt.text_for_voice, callback.message.chat.id)
    db_func.db_set_state(user_id=callback.from_user.id, state='voice_text_for_voice')


@bot.message_handler(state=VoiceSynt.text_for_voice)
def voice_text(message: Message) -> None:

    """
    Обрабатывает сообщения при состоянии VoiceSynt.text_for_voice.
    Принимает и передает в вызываемую функцию voice_text_translation текст для перевода

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    bot.send_message(
        message.chat.id,
        text=f'Принято. Перевожу Ваш текст.'
    )

    voice_text_translation(message)


def voice_text_translation(message: Message) -> None:

    """
    Совершает запрос о переводе к API 'Яндекс.Переводчик' через модуль YaTrnslt_request

    Если запрос неудачный:
        Сообщает о неудаче и предлагает попробовать другой текст

    Иначе:
        Выдает перевод через функцию pretty_text() модуля utils.pretty_translate_YaTrnslt
        Передает перевод и язык в voice_voice_synthesize для озвучивания
        А также вносит запрос типа 'voice' в историю запросов.

    Parameter:
        source_language (str) - Язык переводимого текста
        target_language (str) - Выбранный для перевода язык
        lookup_response (<class 'requests.models.Response'>) - Результат запроса о переводе
        pretty_translation (str) - Приведенный к нужному для вывода пользователю виду результат перевода

    Args:
        message (Message) - Сообщение пользователя

    Returns:
        None
    """

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        source_language = data.get('source_language')
        target_language = data.get('target_language')
        if target_language is None:
            target_language = data.get('voice_target_language')

    lookup_response = yatrnslt_translate(
        text=message.text,
        target_language=target_language,
        source_language=source_language
    )

    if lookup_response.status_code != 200:
        bot.send_message(message.chat.id, text=f'Не удалось выполнить перевод.\n'
                                               f'Попробуйте другой текст.')

    else:

        pretty_translation = pretty_text(
            translate_json=lookup_response.json(),
            text_for_translation=message.text
        )

        bot.send_message(
            message.chat.id,
            text=pretty_translation[0] + '\n\nПроизвожу озвучивание перевода Вашего текста.'
        )

        db_func.db_add_to_history(
            user_id=message.from_user.id,
            operation_type='voice',
            operation_language=target_language,
            operation_text=message.text,
            operation_translate=pretty_translation[1],
            operation_datetime=f'{datetime.now()}'
        )

        voice_voice_synthesize(
            user_id=message.from_user.id,
            voice_translate=pretty_translation[1],
            voice_language=target_language
        )


def voice_voice_synthesize(user_id: int, voice_translate: str, voice_language: str) -> None:

    """
    Совершает запрос о синтезе озвучивания к 'Yandex.Speechkit' через модуль YaSpeechkitSynt_request

    Создает и записывает во временный файл результат запроса.
    Отпраляет голосовое сообщение с результатом пользователю, после чего удаляет временный файл.
    Выдает клавиатуру, предлагает выбрать новый язык (возвращает к custom_to_voice_main) или выйти в главное меню.
    Или ввести новое сообщение
    (т.к. состояние остается VoiceSynt.text_for_voice - следующие сообщения будут обрабатываться voice_text).

    Args:
        user_id (int) - User_id
        voice_translate (str) - Результат перевода
        voice_language (str) - Язык перевода

    Returns:
        None
    """

    with open(f'{TEMP_AUDIO_PATH}{sep}audio_user_id_{user_id}.ogg', "wb") as audio_file:
        for audio_content in synthesize(text=voice_translate, language=voice_language):
            audio_file.write(audio_content)

    with open(f'{TEMP_AUDIO_PATH}{sep}audio_user_id_{user_id}.ogg', 'rb') as voice:
        bot.send_voice(user_id, voice)

    bot.send_message(
        user_id,
        text='Можете написать еще текст или выбрать действие на кнопках.',
        reply_markup=custom_exit_or_select_markup(),
    )

    remove(path=f'{TEMP_AUDIO_PATH}{sep}audio_user_id_{user_id}.ogg')
