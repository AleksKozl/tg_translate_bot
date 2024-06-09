from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def low_exit_or_select_markup():
    keyboard = InlineKeyboardMarkup(row_width=2)

    button_main_menu = InlineKeyboardButton(text='Выйти в главное меню', callback_data='main_menu')
    button_select_language = InlineKeyboardButton(text='Выбрать язык', callback_data='low')

    keyboard.add(button_main_menu, button_select_language)

    return keyboard
