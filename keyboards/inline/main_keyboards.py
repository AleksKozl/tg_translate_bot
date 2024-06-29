from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_markup() -> InlineKeyboardMarkup:

    """
    Создает клавиатуру-главное меню.

    Parameter:
        keyboard (InlineKeyboardMarkup) - Объект клавиатуры
        button_xxx (InlineKeyboardButton) - Объекты кнопок

    Returns:
        <class InlineKeyboardMarkup>
    """

    keyboard = InlineKeyboardMarkup(row_width=1)

    button_help = InlineKeyboardButton(text='Что умеет этот бот?', callback_data='help')
    button_history = InlineKeyboardButton(text='Показать историю запросов.', callback_data='history')
    button_low = InlineKeyboardButton(text='Выполнить перевод отдельного слова.', callback_data='low')
    button_high = InlineKeyboardButton(text='Выполнить перевод текста.', callback_data='high')
    button_custom = InlineKeyboardButton(text='Дополнительные функции', callback_data='custom')

    keyboard.add(button_help, button_history, button_low, button_high, button_custom)
    return keyboard


def to_main_menu_markup() -> InlineKeyboardMarkup:

    """
    Создает клавиатуру для выхода главное меню.

    Parameter:
        keyboard (InlineKeyboardMarkup) - Объект клавиатуры
        button_xxx (InlineKeyboardButton) - Объекты кнопок

    Returns:
        <class InlineKeyboardMarkup>
    """

    keyboard = InlineKeyboardMarkup(row_width=1)

    button_main_menu = InlineKeyboardButton(text='Выйти в главное меню', callback_data='main_menu')

    keyboard.add(button_main_menu)
    return keyboard
