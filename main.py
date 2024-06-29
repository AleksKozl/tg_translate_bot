from telebot.custom_filters import StateFilter

from database.db_func import db_create_tables
from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    db_create_tables()
    bot.polling()
