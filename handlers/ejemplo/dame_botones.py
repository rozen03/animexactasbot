#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update)
from telegram.ext import CallbackContext


def dame_botones(update: Update, context: CallbackContext):
    botones = [[
        InlineKeyboardButton(
            text="boton 1", callback_data=f"dame_botones|mandril"),
        InlineKeyboardButton(
            text="boton 2", callback_data=f"dame_botones|milanesa")
    ]]
    reply_markup = InlineKeyboardMarkup(botones)
    update.message.reply_text(
        "Hola, tomá estos botones :D",
        reply_markup=reply_markup
    )
