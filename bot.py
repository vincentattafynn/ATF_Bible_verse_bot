from decouple import config
from telegram import Update
from telegram.ext import Application, CommandHandler, filters, ContextTypes
import telebot
import time 
import requests

BOT_TOKEN = config('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

#basic intro when the user enters hits start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = time.localtime()

    hour = t.tm_hour

    if 5 <= hour < 12:
        greeting = "Hello, {update.message.chat.id} good morning"
    elif 12 <= hour < 17:
        greeting = f"Hello, {update.message.chat.id} good afternoon"
    else:
        greeting = "Hello, {update.message.chat.id} good evening"
    await update.message.reply_text(f"{greeting}, How are you today? I am a bot that gives you any Bible verse you want")

#functions that gets verse the user wants and extracts its for them
async def verse_getter(verse: str) -> str:
    verse: str = verse.lower() 
    url = "https://bible-api.com/" + verse
    response = requests.get(url)
    response_json = response.json()
    await verse.message.reply_text(f"{response_json['text']}")

bot.infinity_polling()