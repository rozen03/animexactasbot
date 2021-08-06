#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (Update)
from telegram.ext import CallbackContext,CommandHandler

from handlers.basehandler import BaseHandler
from usecases.polls.create_poll import *


class VotarHandler(BaseHandler):
    """Implement handlers for voting"""
    @staticmethod
    def build_handler():
        return CommandHandler('votar', votar)

    @staticmethod
    def command_name():
        return "votar"

    @staticmethod
    def command_description():
        return "Entrega opciones para votar"

def votar(update: Update, context: CallbackContext):
    update.message.reply_text("Yo ya gané")
