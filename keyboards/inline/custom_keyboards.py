from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


"""
Модуль клавиатур к сценарию 'custom'
"""


def custom_high_to_voice_markup() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для выбора действия внутри сценария "custom".

    Parameter:
        keyboard (InlineKeyboardMarkup) - Объект клавиатуры
        button_xxx (InlineKeyboardButton) - Объекты кнопок

    Returns:
        <class InlineKeyboardMarkup>
    """

    keyboard = InlineKeyboardMarkup(row_width=1)

    button_yes = InlineKeyboardButton(text='Да, выбрать язык перевода', callback_data='voice')
    button_no = InlineKeyboardButton(text='Нет, вернуться в главное меню', callback_data='main_menu')

    keyboard.add(button_yes, button_no)
    return keyboard


def custom_languages_markup() -> InlineKeyboardMarkup:

    """
    Создает клавиатуру по выбору языка перевода.

    Parameter:
        keyboard (InlineKeyboardMarkup) - Объект клавиатуры
        button_xxx (InlineKeyboardButton) - Объекты кнопок

    Returns:
        <class InlineKeyboardMarkup>
    """

    keyboard = InlineKeyboardMarkup(row_width=1)

    button_ru = InlineKeyboardButton(text='Перевести на Русский', callback_data='voice_ru')
    button_en = InlineKeyboardButton(text='Перевести на Английский', callback_data='voice_en')
    button_de = InlineKeyboardButton(text='Перевести на Немецкий', callback_data='voice_de')
    button_main_menu = InlineKeyboardButton(text='Выйти в главное меню', callback_data='main_menu')

    keyboard.add(button_ru, button_en, button_de, button_main_menu)

    return keyboard


def custom_main_markup() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для выбора действия внутри сценария "custom".

    Parameter:
        keyboard (InlineKeyboardMarkup) - Объект клавиатуры
        button_xxx (InlineKeyboardButton) - Объекты кнопок

    Returns:
        <class InlineKeyboardMarkup>
    """

    keyboard = InlineKeyboardMarkup(row_width=1)

    button_image = InlineKeyboardButton(text='Определение текста на изображении', callback_data='image')
    button_voice = InlineKeyboardButton(
        text='Перевод с озвучиванием результата\n'
             '(Доступно только для Русского, Английского и Немецкого языков)',
        callback_data='voice'
    )

    keyboard.add(button_image, button_voice)
    return keyboard


def custom_exit_or_select_markup() -> InlineKeyboardMarkup:

    """
    Создает клавиатуру с выбором действия - "Выход в главное меню" или "Смена языка".

    Parameter:
        keyboard (InlineKeyboardMarkup) - Объект клавиатуры
        button_xxx (InlineKeyboardButton) - Объекты кнопок

    Returns:
        <class InlineKeyboardMarkup>
    """

    keyboard = InlineKeyboardMarkup(row_width=1)

    button_main_menu = InlineKeyboardButton(text='Выйти в главное меню', callback_data='main_menu')
    button_select_language = InlineKeyboardButton(text='Выбрать язык', callback_data='voice')

    keyboard.add(button_main_menu, button_select_language)

    return keyboard


def custom_image_translation_language() -> InlineKeyboardMarkup:

    """
    Создает клавиатуру с выбором действия -
    "Выход в главное меню" или "Перевод распознанного текста" (переход к сценарю "high").

    Parameter:
        keyboard (InlineKeyboardMarkup) - Объект клавиатуры
        button_xxx (InlineKeyboardButton) - Объекты кнопок

    Returns:
        <class InlineKeyboardMarkup>
    """

    keyboard = InlineKeyboardMarkup(row_width=1)

    button_image_to_high = InlineKeyboardButton(text='Перевести обнаруженный текст', callback_data='image_to_high')
    button_main_menu = InlineKeyboardButton(text='Выйти в главное меню', callback_data='main_menu')

    keyboard.add(button_image_to_high, button_main_menu)

    return keyboard
