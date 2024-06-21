from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


"""
Модуль клавиатур к сценарию 'high'
"""


def high_exit_or_select_markup() -> InlineKeyboardMarkup:

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
    button_select_language = InlineKeyboardButton(text='Выбрать язык', callback_data='high')
    button_select_voice = InlineKeyboardButton(
        text='Озвучить перевод',
        callback_data='high_to_voice'
    )

    keyboard.add(button_main_menu, button_select_language, button_select_voice)

    return keyboard


def high_languages_markup() -> InlineKeyboardMarkup:

    """
    Создает клавиатуру по выбору языка перевода.

    Parameter:
        keyboard (InlineKeyboardMarkup) - Объект клавиатуры
        button_xxx (InlineKeyboardButton) - Объекты кнопок

    Returns:
        <class InlineKeyboardMarkup>
    """

    keyboard = InlineKeyboardMarkup(row_width=2)

    button_ru = InlineKeyboardButton(text='Русский', callback_data='ru')
    button_en = InlineKeyboardButton(text='Английский', callback_data='en')
    button_de = InlineKeyboardButton(text='Немецкий', callback_data='de')
    button_fr = InlineKeyboardButton(text='Французский', callback_data='fr')
    button_all = InlineKeyboardButton(text='Вывести все варианты', callback_data='all')

    keyboard.add(button_ru, button_en, button_de, button_fr, button_all)

    return keyboard


def high_source_language_markup() -> InlineKeyboardMarkup:

    """
    Создает клавиатуру с которой предлагается выбрать вводить или нет язык переводимого текста.

    Parameter:
        keyboard (InlineKeyboardMarkup) - Объект клавиатуры
        button_xxx (InlineKeyboardButton) - Объекты кнопок

    Returns:
        <class InlineKeyboardMarkup>
    """

    keyboard = InlineKeyboardMarkup(row_width=2)

    button_yes = InlineKeyboardButton(text='Да', callback_data='source_language_yes')
    button_no = InlineKeyboardButton(text='Нет', callback_data='source_language_no')

    keyboard.add(button_yes, button_no)

    return keyboard
