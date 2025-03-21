from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
from google_sheet_reader import *

TOKEN: Final = "7972545280:AAFa83pjZYcwTVYHFruGadbOntX3S_0GE7o"
BOT_USERNAME: Final = "@Little_Botbot"


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! What do you want to talk about?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I can do the following for now:\n"
                                    "To return an item: Type \"return (Asset Tag)\"\n"
                                    "To borrow an item: Type \"borrow (Asset Tag) (Name) (Location)\"")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("What kind of special command are we talking about?")

# Responses

def handle_response(text: str) -> str:
    processed: str = text.lower()
    words: list = processed.split()

    if 'return' in processed:
        asset: int = words[-1]
        return return_item(asset)
    elif 'borrow' in processed:
        asset: int = words[-3]
        name: int = words[-2]
        location: int = words[-1]
        return borrow_item(asset, name, location)
    else:
        return processed




async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval = 3)



