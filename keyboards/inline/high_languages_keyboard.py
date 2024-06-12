from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


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
