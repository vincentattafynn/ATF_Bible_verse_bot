from decouple import config
import telebot

BOT_TOKEN = config('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start','hello'])
def send_welcom(message):
    bot.reply_to(message, "Helo, how are you doing?")

@bot.message_handler(func=lambda msg:True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
