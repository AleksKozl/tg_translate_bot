from telebot.handler_backends import State, StatesGroup


class WordTranslate(StatesGroup):
    language = State()
    word = State()
    word_translate = State()
