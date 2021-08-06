#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update)
from telegram.ext import CallbackContext,CommandHandler

from handlers.basehandler import BaseHandler


class DameBotonesHandler(BaseHandler):
    """Implement handlers for poll creation"""
    @staticmethod
    def build_handler():
        return CommandHandler('damebotones', dame_botones)

    @staticmethod
    def command_name():
        return "damebotones"

    @staticmethod
    def command_description():
        return "Da botones y descubre cosas sobre tu persona al usarlos"
    


def dame_botones(update: Update, context: CallbackContext):
    botones = [[
        InlineKeyboardButton(
            text="boton 1", callback_data="dame_botones|mandril"),
        InlineKeyboardButton(
            text="boton 2", callback_data="dame_botones|milanesa")
    ]]
    reply_markup = InlineKeyboardMarkup(botones)
    update.message.reply_text(
        "Hola, tomá estos botones :D",
        reply_markup=reply_markup
    )
