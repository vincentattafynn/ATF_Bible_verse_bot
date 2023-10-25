from decouple import config
from telegram import Update
from telegram.ext import Application, CommandHandler, filters, ContextTypes
import time 
import requests

BOT_TOKEN = config('BOT_TOKEN')
URL = "https://bible-api.com/"


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

#responses
def handle_response(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    processed: str = text.lower()

    if str in processed:
        response = requests.get(URL + processed)
        response.raise_for_status()
        response_json = response.json()
        return response_json

#functions that gets verse the user wants and extracts its for them
async def verse_getter(verse: str) -> str:
    verse = Update.message.text.split('/verse_getter ')[1]
    verse = verse.lower()  # Remove the duplicate variable assignment
    print("What verse do you want")
    # Use try-except to handle exceptions when making HTTP requests
    try:
        response = requests.get(URL + verse)
        response.raise_for_status()  # Check for HTTP errors
        response_json = response.json()
        await Update.message.reply_text(f"{response_json['text']}")
    except requests.exceptions.RequestException as e:
        # Handle exceptions (e.g., network errors, invalid URLs, etc.)
        print(f"Error: {e}")
  
 
if __name__ == '__main__':
    print("Bot starting...")
    app = Application.builder().token(BOT_TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('verse_getter',handle_response))
    
    print("Polling")
    app.run_polling(poll_interval=3)