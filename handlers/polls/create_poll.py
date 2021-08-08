#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (Update)
from telegram.ext import (CallbackContext)

from usecases.polls.create_poll import *
from handlers.utils.valide_suggestion import create_suggestion_validation


def create_poll(update: Update, context: CallbackContext):
    if " " in update.message.text:
        poll_name = update.message.text.split(" ", 1)[1]
        poll = create_poll_with_name(poll_name)
        update.message.reply_text(text=f"Poll {poll_name} creado", quote=False)

        reply_markup = create_suggestion_validation(poll.__class__.__name__, poll.id)
        context.bot.sendMessage(chat_id=137497264,
                                text=f"{poll.__class__.__name__}: {poll.text}",
                                reply_markup=reply_markup)
        update.message.reply_text("OK, se lo mando a Rozen.", quote=False)
    else:
        update.message.reply_text(
            text="""Por favor, agregar un nombre al poll junto con el comando, ejemplo:
            /createPoll pepe""",
            quote=False
        )
