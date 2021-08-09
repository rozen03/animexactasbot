#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import Update
from telegram.ext import CallbackContext

from usecases.misc.validate_model import validate_model


def validate_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    button_type = context.user_data["button_reply_1"]
    object_id = int(context.user_data["button_reply_2"])
    accept = int(context.user_data["button_reply_3"])
    if accept == 0:
        validate_model(button_type, object_id)
        query.message.edit_text(query.message.text + "\n Aceptado!")
    else:
        query.message.edit_text(query.message.text + "\n Rechazado!")
