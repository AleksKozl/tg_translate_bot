from telebot.async_telebot import AsyncTeleBot
from telebot.storage import StateMemoryStorage

from config_data import config


storage = StateMemoryStorage()

bot = AsyncTeleBot(token=config.BOT_TOKEN, state_storage=storage)
