#!/usr/bin/python3
# -*- coding: utf-8 -*-


import logging

from random import seed

import telegram
from telegram import (ChatAction, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, Update, constants)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler, Updater)

from handlers.polls.create_poll import *

# Local imports
from errors import error_callback
from handlers.button.button_handler import button_handler,te_doy_botones
from handlers.ejemplo.dame_botones import dame_botones
import models

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('animexactasbot.log')

#Made this way not to use db
descriptions = {
        "help" : "Da una lista de comandos basicos",
        "crearpoll" : "Permite crear una nueva encuesta",
        "damebotones" : "Da botones y descubre cosas sobre tu persona al usarlos"
}


def start(update: Update, context: CallbackContext) -> int:
    print(update)
    update.message.reply_text("Hola este es un mensaje de inicio, que se yo")


def help(update: Update, context: CallbackContext):
    message_text = ""
    for command,description in descriptions.items():
        message_text +=  f'/{command} - {description}\n'
    msg = update.message.reply_text(message_text, quote=False)


def estas_vivo(update: Update, context: CallbackContext):
    msg = update.message.reply_text(
        text="Si, estoy vivo",
        quote=False
    )


def iniciar_poll(update: Update, context: CallbackContext):
    with models.db_session:
        pass


def main():
    try:
        # Telegram bot Authorization Token
        botname = "ANIMEXACTASBOT"
        print("Iniciando ANIMEXACTASBOT")
        logger.info("Iniciando")
        models.init_db("animexactasbot.sqlite3")
        updater = Updater(token=token, use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_error_handler(error_callback)

        # Commands
        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)

        estasvivo_handler = CommandHandler('estasvivo', estas_vivo, run_async=True)
        dispatcher.add_handler(estasvivo_handler)

        help_handler = CommandHandler('help', help)
        dispatcher.add_handler(help_handler)

        iniciar_poll_handler = CommandHandler('iniciarpoll', iniciar_poll)
        dispatcher.add_handler(iniciar_poll_handler)

        damebotones_handler = CommandHandler('damebotones', dame_botones)
        dispatcher.add_handler(damebotones_handler)

        create_poll_handler = CommandHandler(['crearpoll','createPoll'], create_poll)
        dispatcher.add_handler(create_poll_handler)
        
        dispatcher.add_handler(CallbackQueryHandler(te_doy_botones, run_async=True, pattern='^' + "dame_botones"))
        
        dispatcher.add_handler(CallbackQueryHandler(button_handler, run_async=True))
        # Start running the bot
        updater.start_polling()
    except Exception as inst:
        logger.critical("ERROR AL INICIAR EL ANIMEXACTASBOT")
        logger.exception(inst)


if __name__ == '__main__':
    from tokenz import *
    main()
