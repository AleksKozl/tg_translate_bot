from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def high_source_language_markup() -> InlineKeyboardMarkup:

    """
    Создает клавиатуру, с которой предлагается выбрать вводить или нет язык переводимого текста.

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
