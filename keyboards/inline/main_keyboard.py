from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_markup():
    keyboard = InlineKeyboardMarkup(row_width=1)

    button_help = InlineKeyboardButton(text='Что умеет этот бот?', callback_data='help')
    button_history = InlineKeyboardButton(text='Показать историю поиска?', callback_data='history')
    button_low = InlineKeyboardButton(text='Выполнить перевод по "Яндекс.Словарю"', callback_data='low')
    button_high = InlineKeyboardButton(text='Выполнить перевод по "Яндекс.Переводчику"', callback_data='high')
    button_custom = InlineKeyboardButton(text='Выполнить перевод с указанием результата', callback_data='custom')

    keyboard.add(button_help, button_history, button_low, button_high, button_custom)
    return keyboard