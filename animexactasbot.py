#!/usr/bin/python3
# -*- coding: utf-8 -*-


import datetime
import logging

from telegram import (Update)
from telegram.botcommand import BotCommand
from telegram.ext import (CallbackContext, CommandHandler, Updater)

# Local imports
import models
from config import config
from errors import error_callback
from handlers.basehandler import BaseHandler
from handlers import *
from handlers.polls.ranking import job_rank_polls

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('animexactasbot.log')

# Made this way not to use db
descriptions={'help':'Da una lista de comandos básicos'}

def help_message(update: Update, context: CallbackContext):
    message_text = ""
    for command, description in descriptions.items():
        message_text += f'/{command} - {description}\n'
    update.message.reply_text(message_text, quote=False)


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

        # Commands
        help_handler = CommandHandler('help', help_message)
        dispatcher.add_handler(help_handler)

        updater.job_queue.run_daily(callback=job_rank_polls, time=datetime.time())

        for command_handler in BaseHandler.__subclasses__():
            dispatcher.add_handler(command_handler.build_handler())
            if command_handler.has_description():
                descriptions[command_handler.command_name()]=command_handler.command_description()
                print(command_handler.command_name())

        dispatcher.bot.set_my_commands(get_command_list())
        # Start running the bot
        updater.start_polling()
    except Exception as inst:
        logger.critical("ERROR AL INICIAR EL ANIMEXACTASBOT")
        logger.exception(inst)


if __name__ == '__main__':
    main()
