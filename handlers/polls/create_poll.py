import telegram
from telegram import (ChatAction, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, Update, constants)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler, Updater)


from usecases.polls.create_poll import *

def create_poll(update: Update, context: CallbackContext):
    if " " in update.message.text:
        poll_name=create_poll_with_name(update.message.text)
        msg = update.message.reply_text(
            text= f"Poll {poll_name} creado",
            quote=False
        )
    else:
        msg = update.message.reply_text(
            text= f"Por favor, agregar un nombre al poll junto con el comando, ejemplo:\n/createPoll pepe",
            quote=False
        )