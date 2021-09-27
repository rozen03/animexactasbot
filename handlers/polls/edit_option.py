#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

import telegram
from telegram import (Update, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (CallbackContext, ConversationHandler)

from handlers.utils.utils import obtener_botonera_polls
from usecases.misc.user import save_user_from_message
from usecases.polls.edit_option import (get_opt_by_id, update_opt)

logger = logging.getLogger('animexactasbot.log')

O_ID, O_EDIT = range(2)

def get_edit_polls(update: Update, context: CallbackContext):
    save_user_from_message(update, context)
    reply_markup = obtener_botonera_polls("get_option")
    print(reply_markup)
    update.message.reply_text(
        "¿Poll con la opción a editar?",
        reply_markup=reply_markup,
    )
    return O_ID

def get_option(update: Update, context: CallbackContext):
    query = update.callback_query
    callback_args = query.data.split("|")

    poll_name = callback_args[1]
    context.user_data['poll_id'] = callback_args[2]

    query.message.reply_text(
        f'Elegiste el poll de {poll_name}.\n\n'
        'Ingresá ahora el id de la opción a editar.'
    )

    try:
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    finally:
        pass

def field_to_edit(update: Update, context: CallbackContext):
    o_id = update.message.text
    print(o_id)
    try:
        opt_id = int(o_id)
        context.user_data["opt_id"] = o_id
    except:
        update.message.reply_text("Id inválido. Operación cancelada.")
        return ConversationHandler.END

    if context.user_data['poll_id'] != str(get_opt_by_id(int(o_id)).poll.id):
        update.message.reply_text("Id no perteneciente a la poll seleccionada.\n\n"
            "Operación cancelada.")
        return ConversationHandler.END

    botones = []
    botones.append(InlineKeyboardButton(text="Text",
        callback_data=f"edit_opt_field|0|{o_id}"))
    botones.append(InlineKeyboardButton(text="Url",
        callback_data=f"edit_opt_field|1|{o_id}"))

    reply_markup = InlineKeyboardMarkup([botones])
    print(reply_markup)
    update.message.reply_text(
        "¿Campo a editar de la opción?",
        reply_markup=reply_markup,
    )
    return O_EDIT

def edit_opt_field(update: Update, context: CallbackContext):
    query = update.callback_query
    callback_args = query.data.split("|")

    context.user_data["field_id"] = callback_args[1]
    opt = get_opt_by_id(context.user_data["opt_id"])
    if (context.user_data["field_id"] == '0'):
        current_val = opt.text
    else:
        current_val = opt.url

    query.message.reply_text(
        f'El valor actual del campo es {current_val}.\n\n'
        'Ingresá ahora el nuevo valor.'
    )

    try:
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    finally:
        pass

def opt_new_value(update: Update, context: CallbackContext) -> int:
    option = update_opt(context.user_data, update.message.text)
  
    update.message.reply_text("Opción editada")

    return ConversationHandler.END