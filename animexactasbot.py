#!/usr/bin/python3
# -*- coding: utf-8 -*-


import datetime

import logging

import pytz
import telegram.ext
from telegram import (Update)
from telegram.botcommand import BotCommand
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler, Updater)

# Local imports
import models
from config import config
from errors import error_callback
from handlers.button.validate_button import validate_button
from handlers.custom_handlers.buttoncallbackqueryhandler import ButtonCallbackQueryHandler
from handlers.button.button_handler import button_handler, te_doy_botones
from handlers.ejemplo.dame_botones import dame_botones
from handlers.polls.create_poll import create_poll
from handlers.polls.ranking import (
    command_rank_polls,
    job_rank_polls,
    get_ranking,
    get_ranking_polls, job_send_votes
)
from handlers.polls.sugerir_opcion import (
    NOMBRE, LINK,
    nombre,
    link,
    cancelar,
    polls_reply,
    sugerir_opcion
)
from handlers.ejemplo.votar import (
    votar,
    votar_opciones,
    opcion_votada
)
from handlers.polls.listar import (
    get_polls,
    listar_polls
)

from handlers.polls.edit_option import (
    O_ID, O_EDIT,
    get_edit_polls,
    get_option,
    field_to_edit,
    edit_opt_field,
    opt_new_value
)


# Enable logging
from usecases.misc.user import save_user_from_message, save_user_from_button

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO, filename="animexactasbot.log"
)

logger = logging.getLogger('animexactasbot.log')

# Made this way not to use db
descriptions = {
    "help": "Da una lista de comandos básicos",
    "crearpoll": "Permite crear una nueva encuesta",
    "damebotones": "Da botones y descubre cosas sobre tu persona al usarlos",
    "sugeriropcion": "Permite sugerir una opción para alguna poll",
    "votar": "Te deja votar entre 2 opciones de una poll, vota bien (?)"
}


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hola este es un mensaje de inicio, que se yo")


def help_message(update: Update, context: CallbackContext):
    message_text = ""
    for command, description in descriptions.items():
        message_text += f'/{command} - {description}\n'
    update.message.reply_text(message_text, quote=False)


def estas_vivo(update: Update, context: CallbackContext):
    update.message.reply_text(text="Si, estoy vivo", quote=False)


def get_command_list():
    return [BotCommand(command, description) for command, description in descriptions.items()]


def main():
    # noinspection Pylint
    try:
        # Telegram bot Authorization Token
        print("Iniciando ANIMEXACTASBOT")
        logger.info("Iniciando")
        models.init_db("animexactasbot.sqlite3")

        updater = Updater(token=config["TOKEN"], use_context=True)

        dispatcher = updater.dispatcher
        dispatcher.add_error_handler(error_callback)
        # TODO: create a different handler, i was really sleepy
        dispatcher.add_handler(MessageHandler(filters=telegram.ext.Filters.all,
                                              callback=save_user_from_message), group=1)
        dispatcher.add_handler(CallbackQueryHandler(save_user_from_button), group=1)
        # Commands
        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)

        dispatcher.add_handler(CommandHandler('estasvivo', estas_vivo, run_async=True))

        help_handler = CommandHandler('help', help_message)
        dispatcher.add_handler(help_handler)

        dispatcher.add_handler(CommandHandler('damebotones', dame_botones))

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

        votar_opciones_handler = ButtonCallbackQueryHandler(
            votar_opciones,
            run_async=True,
            pattern='^' + "(votar_opciones|dame_otro)"
        )
        dispatcher.add_handler(votar_opciones_handler)

        opcion_votada_handler = ButtonCallbackQueryHandler(
            opcion_votada,
            run_async=True,
            pattern='^' + "opcion_votada"
        )
        dispatcher.add_handler(opcion_votada_handler)

        te_doy_botones_handler = ButtonCallbackQueryHandler(
            te_doy_botones,
            run_async=True,
            pattern='^' + "dame_botones"
        )
        dispatcher.add_handler(te_doy_botones_handler)

        validate_button_handler = ButtonCallbackQueryHandler(
            validate_button,
            run_async=True,
            pattern='^' + "validate_button"
        )
        dispatcher.add_handler(validate_button_handler)

        get_ranking_handler = ButtonCallbackQueryHandler(
            get_ranking,
            run_async=True,
            pattern='^' + "get_ranking"
        )
        dispatcher.add_handler(get_ranking_handler)

        list_polls_handler = ButtonCallbackQueryHandler(
            listar_polls,
            run_async=True,
            pattern='^' + "listar_polls"
        )
        dispatcher.add_handler(list_polls_handler)

        edit_opcion_handler = ConversationHandler(
            entry_points=[CommandHandler('editopt', get_edit_polls)],
            states={
                O_ID: [MessageHandler(Filters.text & ~Filters.command, field_to_edit)],
                O_EDIT: [MessageHandler(Filters.text & ~Filters.command, opt_new_value)]
            },
            fallbacks=[CommandHandler('cancelar', cancelar)]
        )
        dispatcher.add_handler(edit_opcion_handler)

        get_option_handler = ButtonCallbackQueryHandler(
            get_option,
            run_async=True,
            pattern='^' + "get_option"
        )
        dispatcher.add_handler(get_option_handler)

        edit_option_field_handler = ButtonCallbackQueryHandler(
            edit_opt_field,
            run_async=True,
            pattern='^' + "edit_opt_field"
        )
        dispatcher.add_handler(edit_option_field_handler)


        updater.job_queue.run_daily(callback=job_rank_polls, time=datetime.time())

        manual_rank_polls = CommandHandler('rankeameloh', command_rank_polls, run_async=True)
        dispatcher.add_handler(manual_rank_polls)

        dispatcher.add_handler(CommandHandler('ranking', get_ranking_polls, run_async=True))

        dispatcher.add_handler(CommandHandler('listar', get_polls, run_async=True))

        for hour in [9, 13, 17, 21]:
            updater.job_queue.run_daily(callback=job_send_votes,
                                        time=datetime.time(hour=hour, minute=0, second=0,
                                                           tzinfo=pytz.timezone(
                                                               'America/Argentina/Buenos_Aires')))
        dispatcher.bot.set_my_commands(get_command_list())
        # Start running the bot

        # Este es el handler default de botones, si llega acá es que algo salió mal
        dispatcher.add_handler(CallbackQueryHandler(button_handler, run_async=True))
        updater.start_polling()
    except Exception as inst:
        logger.critical("ERROR AL INICIAR EL ANIMEXACTASBOT")
        logger.exception(inst)


if __name__ == '__main__':
    main()
