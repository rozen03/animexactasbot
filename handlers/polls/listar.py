#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram import (Update)
from telegram.ext import (CallbackContext)

from handlers.utils.utils import obtener_botonera_polls
from usecases.misc.user import save_user_from_message

from models import Option, db_session, select

logger = logging.getLogger('animexactasbot.log')

def get_polls(update: Update, context: CallbackContext):
    save_user_from_message(update, context)
    reply_markup = obtener_botonera_polls("listar_polls")
    update.message.reply_text(
        "¿Poll a listar?",
        reply_markup=reply_markup,
    )


def listar_polls(update: Update, context: CallbackContext) -> None:
    print("listing")
    query = update.callback_query
    callback_args = query.data.split("|")

    poll_name = callback_args[1]
    poll_id = callback_args[2]

    opt_list = list_poll_options(poll_id)
    opt_list.sort()

    try:
        query.edit_message_text(text=f'Elegiste el poll de {poll_name}.\n\n')
        txt_msg = ""
        for (name, url) in opt_list:
            if len(txt_msg + f'[{name}]({url})\n') > 4096:
                update.message.reply_text(txt_msg,
                    disable_web_page_preview=True,
                    parse_mode=telegram.ParseMode.MARKDOWN)
                txt_msg = ""
            txt_msg = txt_msg + f'[{name}]({url})\n'

        update.message.reply_text(txt_msg[:-1],
            disable_web_page_preview=True,
            parse_mode=telegram.ParseMode.MARKDOWN)
    finally:
        pass

@db_session
def list_poll_options(poll_id):
    option_list = select((o.text,o.url) for o in Option if o.poll.id == poll_id)[:]
    return option_list