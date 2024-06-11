from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def low_languages_markup() -> InlineKeyboardMarkup:

    """
    Создает клавиатуру по выбору языка перевода.

    Parameter:
        keyboard (InlineKeyboardMarkup) - Объект клавиатуры
        button_xxx (InlineKeyboardButton) - Объекты кнопок

    Returns:
        <class InlineKeyboardMarkup>
    """

    keyboard = InlineKeyboardMarkup(row_width=2)

    button_ru_en = InlineKeyboardButton(text='Русский - Английский', callback_data='ru-en')
    button_en_ru = InlineKeyboardButton(text='Английский - Русский', callback_data='en-ru')
    button_ru_de = InlineKeyboardButton(text='Русский - Немецкий', callback_data='ru-de')
    button_de_ru = InlineKeyboardButton(text='Немецкий - Русский', callback_data='de-ru')
    button_all = InlineKeyboardButton(text='Вывести все варианты', callback_data='all')

    keyboard.add(button_ru_en, button_en_ru, button_ru_de, button_de_ru, button_all)

    return keyboard
