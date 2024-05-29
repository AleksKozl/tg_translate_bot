from telebot.handler_backends import State, StatesGroup


class WordTranslate(StatesGroup):
    language = State()
    langs = State()
    word = State()
    word_tranlate = State()
