import asyncio
from telebot.custom_filters import StateFilter

from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':
    asyncio.run(bot.add_custom_filter(StateFilter(bot)))
    asyncio.run(set_default_commands(bot))
    asyncio.run(bot.polling())
