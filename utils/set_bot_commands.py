from config_data.config import DEFAULT_COMMANDS
from telebot.types import BotCommand


def set_default_commands(bot):
    """ Устанавливает команды бота согласно спику стандартных команд в модуле config_data.config """
    bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])
