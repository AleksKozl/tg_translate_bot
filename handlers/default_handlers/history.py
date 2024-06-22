from telebot.types import CallbackQuery

from states.state_translation import WordTranslate
from loader import bot
from keyboards.inline.main_keyboards import to_main_menu_markup
from database.db_func import db_set_state, db_get_history


@bot.callback_query_handler(func=lambda callback: callback.data == 'history')
def history(callback: CallbackQuery) -> None:
    """
    "Сбрасывает" состояние пользователя и выдает историю запросов.

    Parameter:
        history_all (List[History]) - Список со всеми записями запросов пользователя
        history_text (str) - Строка для удобства отображения запросов.

    Args:
        callback (CallbackQuery) -  Входящий запрос обратного вызова от кнопок на inline клавиатурах

    Returns:
        None
    """

    bot.set_state(callback.from_user.id, WordTranslate.wait, callback.message.chat.id)
    db_set_state(user_id=callback.from_user.id, state='wait')

    history_all = db_get_history(callback.from_user.id)
    history_text = 'Ваша история запросов:\n\n'
    for i_hist in history_all:

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
        reply_markup=to_main_menu_markup()
    )
