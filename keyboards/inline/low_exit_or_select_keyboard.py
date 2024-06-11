from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def low_exit_or_select_markup() -> InlineKeyboardMarkup:

    """
    Создает клавиатуру по с выбором действия - "Выход в главное меню" или "Смена языка".

    Parameter:
        keyboard (InlineKeyboardMarkup) - Объект клавиатуры
        button_xxx (InlineKeyboardButton) - Объекты кнопок

    Returns:
        <class InlineKeyboardMarkup>
    """

    keyboard = InlineKeyboardMarkup(row_width=2)

    button_main_menu = InlineKeyboardButton(text='Выйти в главное меню', callback_data='main_menu')
    button_select_language = InlineKeyboardButton(text='Выбрать язык', callback_data='low')

    keyboard.add(button_main_menu, button_select_language)

    return keyboard
