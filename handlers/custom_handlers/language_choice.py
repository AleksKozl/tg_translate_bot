from telebot.types import Message

from YaAPI.YaDictAPI import YaDict_request
from loader import bot
from states.state_word_translate import WordTranslate
from utils.pretty_translate_YaDict import pretty_translate


# func=lambda message: message.text in ['/language_choice', 'Выбрать направление перевода']
language_selected = None


@bot.message_handler(commands=['language_choice'])
def selection_language(message: Message) -> None:
    langs_response = YaDict_request.get_langs()
    if langs_response.status_code != 200:
        bot.send_message(message.chat.id, text='Не удалось получить список направлений перевода')
        exit(1)

    langs = langs_response.json()

    YaDict_request.langs = langs
    WordTranslate.langs = langs

    buf_langs = ' || '.join(langs) # - Временное решение

    bot.set_state(message.from_user.id, WordTranslate.language, message.chat.id)
    bot.send_message(message.chat.id, text='Выберите одно из доступных направлений перевода')

    bot.send_message(message.chat.id, text=buf_langs) # - Заменить на кнопки с "частыми" / облагородить


@bot.message_handler(state=WordTranslate.language)
def get_language(message: Message) -> None:

    if message.text not in YaDict_request.langs:
        bot.send_message(message.chat.id, text='Такого направления нет. Попробуйте ещё раз')
        selection_language(message)

    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['language'] = message.text

        global language_selected
        language_selected = message.text

        bot.send_message(message.chat.id, text=f'Принято. Ваше направление перевода: {message.text}')
        bot.send_message(message.chat.id, text='Введите слово или фразу для перевода:')

        bot.set_state(message.from_user.id, WordTranslate.word, message.chat.id)


@bot.message_handler(state=WordTranslate.word)
def get_word(message: Message) -> None:

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['word'] = message.text
    bot.send_message(message.chat.id, text=f'Принято. Перевожу: "{message.text}"')
    get_word_translate(message)


@bot.message_handler(state=WordTranslate.word_translate)
def get_word_translate(message: Message) -> None:

    global language_selected
    lookup_response = YaDict_request.lookup(language_selected, message.text)

    if lookup_response.status_code != 200:
        bot.send_message(message.chat.id, text=('Не удалось выполнить перевод:', lookup_response.text))
        exit(1)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['word_translate'] = lookup_response.json()

    temp_answer = ' || '.join(lookup_response.json())

    bot.send_message(message.chat.id, text='Ваш перевод:')
    bot.send_message(message.chat.id, text=pretty_translate(lookup_response.json()))

