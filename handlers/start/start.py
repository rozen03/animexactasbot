from telegram import Update
from telegram.ext import (CallbackContext,CommandHandler)
from handlers.basehandler import BaseHandler

class StartHandler(BaseHandler):
    """Handler for the start command"""
    @staticmethod
    def build_handler():
        return CommandHandler('start', start)

    @staticmethod
    def command_name():
        return "start"

    @staticmethod
    def command_description():
        return "Mensaje de inicio"
    

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hola este es un mensaje de inicio, que se yo")
    