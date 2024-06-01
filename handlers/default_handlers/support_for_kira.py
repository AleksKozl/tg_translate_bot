from telebot.types import Message

from loader import bot


@bot.message_handler(func=lambda message: message.text in ['/support_for_kira', 'Поддержать Киру'])
def support_for_kira(message: Message):
    bot.send_message(message.chat.id, text='Кира, у тебя все получится! Скоро ты поедешь домой!')
