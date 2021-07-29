import telegram
from telegram import (ChatAction, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, Update, constants)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler, Updater)

from pony.orm import db_session
from models import Poll
from enum import Enum, auto

class Period(Enum):
    DAILY=auto()
    WEEKLY=auto()
    MONTHLY=auto()



def create_poll(update: Update, context: CallbackContext):
    if " " in update.message.text:
        poll_name=(update.message.text).split(" ", 1)[1]
        with db_session:
            poll=Poll(text=poll_name,periodic_votes=2,period=Period.WEEKLY.name)
        msg = update.message.reply_text(
            text= f"Poll {poll_name} creado",
            quote=False
        )
    else:
        msg = update.message.reply_text(
            text= f"Por favor, agregar un nombre al poll junto con el comando, ejemplo:\n/createPoll pepe",
            quote=False
        )