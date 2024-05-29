from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def gen_markup():
    button_help = KeyboardButton(text="Что умеет этот бот?")
    button_history = KeyboardButton(text="Показать историю поиска")
    button_history_clean = KeyboardButton(text="Очистить историю поиска")
    button_chat_clean = KeyboardButton(text="Очистить чат")
    button_support_for_kira = KeyboardButton(text="Поддержать Киру")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_help, button_history, button_history_clean, button_chat_clean, button_support_for_kira)
    return keyboard
