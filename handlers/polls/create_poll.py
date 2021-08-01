#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (Update)
from telegram.ext import (CallbackContext)

from usecases.polls.create_poll import *


def create_poll(update: Update, context: CallbackContext):
    if " " in update.message.text:
        poll_name = update.message.text.split(" ", 1)[1]
        create_poll_with_name(poll_name)
        update.message.reply_text(text=f"Poll {poll_name} creado", quote=False)
    else:
        update.message.reply_text(
            text="""Por favor, agregar un nombre al poll junto con el comando, ejemplo:
            /createPoll pepe""",
            quote=False
        )
