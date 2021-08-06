from telegram import Update
from telegram.ext import (CallbackContext,CommandHandler)
from handlers.basehandler import BaseHandler

class EstasVivoHandler(BaseHandler):
    """Handler for the start command"""
    @staticmethod
    def build_handler():
        return CommandHandler('estasvivo', estas_vivo, run_async=True)

    @staticmethod
    def command_name():
        return "estasvivo"

    @staticmethod
    def command_description():
        return "Mensaje para saber si el bot esta vivo"
    
def estas_vivo(update: Update, context: CallbackContext):
    update.message.reply_text(text="Si, estoy vivo", quote=False)
