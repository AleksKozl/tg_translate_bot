from telebot.types import CallbackQuery

from states.state_translation import WordTranslate
from loader import bot
from keyboards.inline.main_keyboards import history_markup
from database.db_func import db_set_state, db_get_history


@bot.callback_query_handler(func=lambda callback: callback.data == 'history')
def main_menu(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопок ведущих в главное меню.
    "Сбрасывает" состояние пользователя и редактирует предыдущее сообщение.
    Выдает клавиатуру-главное меню (main_keyboard.main_markup)

    Returns:
        None
    """

    bot.set_state(callback.from_user.id, WordTranslate.wait, callback.message.chat.id)
    db_set_state(user_id=callback.from_user.id, state='wait')

    history = db_get_history(callback.from_user.id)
    history_text = 'Ваша история запросов:\n\n'
    for i_hist in history:

        operation_text = i_hist.operation_text[:15] + '...' \
            if len(i_hist.operation_text) > 15 \
            else i_hist.operation_text
        operation_translate = i_hist.operation_translate[:15] + '...' \
            if len(i_hist.operation_translate) > 15 \
            else i_hist.operation_translate

        history_text += (
            f'Тип запроса - {i_hist.operation_type}\n'
            f'Язык запроса - {i_hist.operation_language}\n'
            f'Переводимый текст - {operation_text}\n'
            f'Перевод - {operation_translate}\n'
            f'Дата и время запроса - {i_hist.operation_datetime}\n\n'
        )

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=history_text,
        reply_markup=history_markup()
    )
