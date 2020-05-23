from databases import *
import telebot
import time
from telebot import types

bot_token = '1260422753:AAGk_W_MfVoCD-HqTp54cAqTGay34Ll4gs8'

bot = telebot.TeleBot(token=bot_token)


@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "hi yourself")


@bot.message_handler(func=lambda message: message.text == "what's my favorite food?")
def command_text_favorite_food(m):
    favorite_food = sh.sheet1.cell(2, 1).value
    bot.send_message(m.chat.id, "your favorite food is " + favorite_food)


if __name__ == '__main__':
    while True:
        try:
            bot.polling()
        except Exception:
            time.sleep(15)
