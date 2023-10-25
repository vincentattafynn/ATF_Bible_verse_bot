from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import time
import requests
from decouple import config
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN: Final = os.getenv('BOT_TOKEN')

BOT_USERNAME: Final = "@ATF_verse_bot"

URL = "https://bible-api.com/"

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = time.localtime()

    hour = t.tm_hour

    if 5 <= hour < 12:
        greeting = "Hello, {update.message.chat.username} good morning"
    elif 12 <= hour < 17:
        greeting = f"Hello, {update.message.chat.username} good afternoon"
        
    else:
        greeting = "Hello, {update.message.chat.username} good evening"
    
    await update.message.reply_text(f"{greeting}, How are you today? I am a bot that gives you any Bible verse that you request for.Just enter the verse you want and I will send it to you.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("i am just a test bot")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")



#Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    verse = URL + processed


    response = requests.get(verse)
    if response.status_code == 200:
        response_json = response.json()
    else:
        return "You entered an incorrect verse"


    return (f"{response_json['text']}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: {text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')



if __name__ == '__main__':
    print('Starting...')
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    #Error handlers
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling()