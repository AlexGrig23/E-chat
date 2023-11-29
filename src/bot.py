import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext, MessageHandler, filters
from src.send import send_message


load_dotenv()

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}\n'
                                    f'Command: /print - return last message\n'
                                    f'Command: /send - send POST request\n')


async def print_last_message(update: Update, context: CallbackContext) -> None:
    await send_message(command='print', body="".encode('utf-8'))


async def send_last_message(update: Update, context: CallbackContext) -> None:
    await send_message(command='send', body="".encode('utf-8'))


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_message(command=None, body=update.message.text.encode('utf-8'))


app = ApplicationBuilder().token(os.getenv("TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("print", print_last_message))
app.add_handler(CommandHandler("send", send_last_message))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))

