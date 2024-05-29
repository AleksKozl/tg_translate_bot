from loader import bot
from keyboards.reply import main_keyboard


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    text = (
            'Привет!\n'
            'Я бот, который умеет переводить слова на другие языки.\n'
            )
    await bot.send_message(message.from_user.id, text, reply_markup=main_keyboard.gen_markup())
