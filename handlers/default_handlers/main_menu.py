from telebot.types import CallbackQuery

from states.state_translation import WordTranslate
from loader import bot
from keyboards.inline.main_keyboard import main_markup
from database.db_func import db_set_state


@bot.callback_query_handler(func=lambda callback: callback.data == 'main_menu')
def main_menu(callback: CallbackQuery) -> None:

    """
    Обработчик нажатия кнопок клавиатуры (main_keyboard.main_markup).
    "Сбрасывает" состояние пользователя и редактирует предыдущее сообщение.
    Выдает клавиатуру-главное меню (main_keyboard.main_markup)

    Returns:
        None
    """

    bot.set_state(callback.from_user.id, WordTranslate.wait, callback.message.chat.id)
    db_set_state(user_id=callback.from_user.id, state='wait')

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=f'И так, {callback.from_user.first_name}, что мне сделать теперь?\n',
        reply_markup=main_markup()
    )
