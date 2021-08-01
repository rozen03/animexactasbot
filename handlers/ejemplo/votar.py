#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (ChatAction, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, Update, constants)
from telegram.ext import CallbackContext

def votar(update: Update, context: CallbackContext):
    update.message.reply_text("Yo ya gané")