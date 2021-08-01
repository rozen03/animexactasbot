#!/usr/bin/python3
# -*- coding: utf-8 -*-


import logging

from telegram import (Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler, Updater)

# Local imports
import models
from errors import error_callback
from handlers.button.button_handler import button_handler, te_doy_botones
from handlers.ejemplo.dame_botones import dame_botones
from handlers.polls.create_poll import create_poll
from handlers.polls.sugerir_opcion import (
    NOMBRE, LINK,
    nombre,
    link,
    cancelar,
    polls_reply,
    sugerir_opcion
)
from handlers.ejemplo.votar import votar

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('animexactasbot.log')

# Made this way not to use db
descriptions = {
    "help": "Da una lista de comandos básicos",
    "crearpoll": "Permite crear una nueva encuesta",
    "damebotones": "Da botones y descubre cosas sobre tu persona al usarlos"
}


def start(update: Update, context: CallbackContext) -> None:
    print(update)
    update.message.reply_text("Hola este es un mensaje de inicio, que se yo")


def help_message(update: Update, context: CallbackContext):
    message_text = ""
    for command, description in descriptions.items():
        message_text += f'/{command} - {description}\n'
    update.message.reply_text(message_text, quote=False)


def estas_vivo(update: Update, context: CallbackContext):
    update.message.reply_text(text="Si, estoy vivo", quote=False)


def main():
    # noinspection Pylint
    try:
        # Telegram bot Authorization Token
        print("Iniciando ANIMEXACTASBOT")
        logger.info("Iniciando")
        models.init_db("animexactasbot.sqlite3")

        updater = Updater(token=token, use_context=True) # pylint: disable=undefined-variable
        dispatcher = updater.dispatcher
        dispatcher.add_error_handler(error_callback)

        # Commands
        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)

        estasvivo_handler = CommandHandler('estasvivo', estas_vivo, run_async=True)
        dispatcher.add_handler(estasvivo_handler)

        help_handler = CommandHandler('help', help_message)
        dispatcher.add_handler(help_handler)

        damebotones_handler = CommandHandler('damebotones', dame_botones)
        dispatcher.add_handler(damebotones_handler)

        create_poll_handler = CommandHandler(['crearpoll', 'createPoll'], create_poll)
        dispatcher.add_handler(create_poll_handler)

        sugerir_opcion_handler = ConversationHandler(
            entry_points=[CommandHandler('sugeriropcion', sugerir_opcion)],
            states={
                NOMBRE: [MessageHandler(Filters.text & ~Filters.command, nombre)],
                LINK: [MessageHandler(Filters.text & ~Filters.command, link)]
            },
            fallbacks=[CommandHandler('cancelar', cancelar)]
        )

        dispatcher.add_handler(sugerir_opcion_handler)
        polls_reply_handler = CallbackQueryHandler(
            polls_reply,
            run_async=True,
            pattern='^' + "polls_reply"
        )
        dispatcher.add_handler(polls_reply_handler)

        votar_handler = CommandHandler('votar', votar)
        dispatcher.add_handler(votar_handler)

        te_doy_botones_handler = CallbackQueryHandler(
            te_doy_botones,
            run_async=True,
            pattern='^' + "dame_botones"
        )
        dispatcher.add_handler(te_doy_botones_handler)

        dispatcher.add_handler(CallbackQueryHandler(button_handler, run_async=True))
        # Start running the bot
        updater.start_polling()
    except Exception as inst:
        logger.critical("ERROR AL INICIAR EL ANIMEXACTASBOT")
        logger.exception(inst)


if __name__ == '__main__':
    # noinspection Pylint
    from tokenz import *  # pylint: disable=import-error

    main()
