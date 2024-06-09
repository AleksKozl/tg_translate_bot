from telebot.types import Message, CallbackQuery

from YaAPI.YaDictAPI import YaDict_request
from loader import bot
from states.state_word_translate import WordTranslate
from utils.pretty_translate_YaDict import pretty_text
from keyboards.inline import low_languages_keyboard, low_exit_or_select_keyboard
import database.db_func as db_func


@bot.callback_query_handler(func=lambda callback: callback.data == 'low')
def welcome_to_low(callback: CallbackQuery):
    bot.set_state(callback.from_user.id, WordTranslate.wait, callback.message.chat.id)
    db_func.db_set_state(user_id=callback.from_user.id, state='wait')

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text='Выберите одно из доступных направлений перевода:',
        reply_markup=low_languages_keyboard.low_languages_markup()
    )


@bot.callback_query_handler(func=lambda callback: callback.data in ['ru-en', 'en-ru', 'ru-de', 'de-ru', 'all'])
def language_set(callback: CallbackQuery) -> None:
    langs_response = YaDict_request.langs

    if langs_response.status_code != 200:
        bot.send_message(
            callback.message.id,
            text='Не удалось получить список направлений перевода.\n'
                 'Не удачная попытка связи с "Яндекс.Словарь".\n'
                 'Повторите попытку позднее.'
        )
        exit(1)

    if callback.data == 'all':

        buf_langs = ' || '.join(YaDict_request.langs.json())
        bot.send_message(
            callback.message.chat.id,
            text=buf_langs
        )
        bot.send_message(
            callback.message.chat.id,
            text='Напишите выбранное Вами направление как в этих примерах: ru-en, en-ru, en-de'
        )

        bot.set_state(callback.from_user.id, WordTranslate.language, callback.message.chat.id)
        db_func.db_set_state(user_id=callback.from_user.id, state='language')

    elif callback.data in ['ru-en', 'en-ru', 'ru-de', 'de-ru']:

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text=f'Принято. Ваше направление перевода: "{callback.data}"\n'
                 f'Введите слово для перевода:'
        )

        db_func.db_set_language(user_id=callback.from_user.id, language=callback.data)
        bot.set_state(callback.from_user.id, WordTranslate.word, callback.message.chat.id)
        db_func.db_set_state(user_id=callback.from_user.id, state='word')


@bot.message_handler(state=WordTranslate.language)
def language_check(message: Message) -> None:
    if message.text not in YaDict_request.langs.json():
        bot.send_message(message.chat.id, text='Такого направления нет. Попробуйте ещё раз.')

    else:

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=f'Принято. Ваше направление перевода: "{message.text}"\n'
                 f'Введите слово для перевода:'
        )

        db_func.db_set_language(user_id=message.from_user.id, language=message.text)

        bot.set_state(message.from_user.id, WordTranslate.word, message.chat.id)
        db_func.db_set_state(user_id=message.from_user.id, state='word')


@bot.message_handler(state=WordTranslate.word)
def get_word(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['word'] = message.text

    bot.send_message(message.chat.id, text=f'Принято. Перевожу: "{message.text}"')

    bot.set_state(message.from_user.id, WordTranslate.word_translate, message.chat.id)
    db_func.db_set_state(user_id=message.from_user.id, state='word_translate')

    get_word_translate(message)


@bot.message_handler(state=WordTranslate.word_translate)
def get_word_translate(message: Message) -> None:
    language_selected = db_func.db_get_language(user_id=message.from_user.id)
    lookup_response = YaDict_request.lookup(language_selected, message.text)

    if lookup_response.status_code != 200 or len(lookup_response.json()['def']) == 0:
        bot.send_message(message.chat.id, text=f'Не удалось выполнить перевод: "{message.text}"\n'
                                               f'Попробуйте другое слово.')

    else:
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
                text='Можете написать еще одно слово или выбрать действие на кнопках.',
                reply_markup=low_exit_or_select_keyboard.low_exit_or_select_markup()
            )

        bot.set_state(message.from_user.id, WordTranslate.word, message.chat.id)
        db_func.db_set_state(user_id=message.from_user.id, state='word')
