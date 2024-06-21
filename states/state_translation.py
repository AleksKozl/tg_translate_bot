from telebot.handler_backends import State, StatesGroup


class WordTranslate(StatesGroup):

    wait = State()
    language = State()
    numbers_of_translations = State()
    word = State()
    word_translate = State()


class TextTranslate(StatesGroup):

    wait = State()
    target_language = State()
    source_language = State()
    text = State()
    text_translate = State()


class VoiceSynt(StatesGroup):

    wait = State()
    target_language = State()
    text_for_voice = State()
    voice = State()
