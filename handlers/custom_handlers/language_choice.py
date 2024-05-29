from telebot.types import Message

from YaAPI.YaDictAPI import YaDict_request
from loader import bot
from states.state_word_translate import WordTranslate


@bot.message_handler(func=lambda message: message.text in ['/language_choice', 'Выбрать направление перевода'])
async def selection_language(message: Message) -> None:
    langs_response = YaDict_request.get_langs()
    if langs_response.status_code != 200:
        await bot.send_message(message.chat.id, text='Не удалось получить список направлений перевода')
        exit(1)

    langs = langs_response.json()
    await bot.set_state(message.from_user.id, WordTranslate.langs, message.chat.id)

    await bot.send_message(message.chat.id, text='Выберите одно из доступных направлений перевода')

    await bot.send_message(message.chat.id, text=langs) # - Заменить на кнопки с "частыми" / облагородить

    while message.text not in WordTranslate.langs:
        await bot.send_message(message.chat.id, text='Такого направления нет. Попробуйте ещё раз')


@bot.message_handler(state=WordTranslate.language)
async def get_language(message: Message) -> None:
    pass
