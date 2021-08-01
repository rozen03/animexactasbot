#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (Update)
from telegram.ext import CallbackContext


def votar(update: Update, context: CallbackContext):
    update.message.reply_text("Yo ya gané")
