from telebot.types import Message

from YaAPI.YaDictAPI import YaDict_request
from loader import bot
from states.state_word_translate import WordTranslate
from utils.pretty_translate_YaDict import pretty_text
import database.db_func as db_func
from pprint import pprint


@bot.message_handler(commands=['language_choice'])
def selection_language(message: Message) -> None:
    langs_response = YaDict_request.get_langs()

    if langs_response.status_code != 200:
        bot.send_message(message.chat.id, text='Не удалось получить список направлений перевода')
        exit(1)

    langs = langs_response.json()
    YaDict_request.langs = langs

    buf_langs = ' || '.join(langs)  # - Временное решение

    bot.set_state(message.from_user.id, WordTranslate.language, message.chat.id)
    db_func.db_set_state(user_id=message.from_user.id, state='language')

    bot.send_message(message.chat.id, text='Выберите одно из доступных направлений перевода')
    bot.send_message(message.chat.id, text=buf_langs)  # - Заменить на кнопки с "частыми" / облагородить


@bot.message_handler(state=WordTranslate.language)
def get_language(message: Message) -> None:
    if message.text not in YaDict_request.langs:
        bot.send_message(message.chat.id, text='Такого направления нет. Попробуйте ещё раз')
        selection_language(message)

    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['language'] = message.text
            db_func.db_set_language(user_id=message.from_user.id, language=message.text)

        bot.send_message(message.chat.id, text=f'Принято. Ваше направление перевода: {message.text}')
        bot.send_message(message.chat.id, text='Введите слово для перевода:')

        bot.set_state(message.from_user.id, WordTranslate.word, message.chat.id)
        db_func.db_set_state(user_id=message.from_user.id, state='word')


@bot.message_handler(state=WordTranslate.word)
def get_word(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['word'] = message.text
        # db_func.db_add_word(message.text)

    bot.send_message(message.chat.id, text=f'Принято. Перевожу: "{message.text}"')

    bot.set_state(message.from_user.id, WordTranslate.word_translate, message.chat.id)
    db_func.db_set_state(user_id=message.from_user.id, state='word_translate')
    get_word_translate(message)


@bot.message_handler(state=WordTranslate.word_translate)
def get_word_translate(message: Message) -> None:
    language_selected = db_func.db_get_language(user_id=message.from_user.id)
    lookup_response = YaDict_request.lookup(language_selected, message.text)

    pprint(lookup_response.json()['def'])

    if lookup_response.status_code != 200 or len(lookup_response.json()['def']) == 0:
        bot.send_message(message.chat.id, text=('Не удалось выполнить перевод:', message.text))

        bot.set_state(message.from_user.id, WordTranslate.word, message.chat.id)
        db_func.db_set_state(user_id=message.from_user.id, state='word')

        bot.send_message(message.chat.id, text='Попробуйте другое слово.')
        exit(1)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['word_translate'] = lookup_response.json()
        db_func.db_add_word(data['word'])

        bot.send_message(
            message.chat.id,
            text=pretty_text(
                word=message.text,
                language=db_func.db_get_language(user_id=message.from_user.id),
                translate_json=data['word_translate']
            )
        )

        bot.send_message(
            message.chat.id,
            text='Напишите ещё одно слово'
        )

    bot.set_state(message.from_user.id, WordTranslate.word, message.chat.id)
