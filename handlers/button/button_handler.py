#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardMarkup, Update
from telegram.ext.callbackcontext import CallbackContext

# noinspection Pylint
""" 
This handler main idea es to handle any button pressed by the user.
Every Button comes with callback_data, let's have a common ground of how to deal with them:
    - Any callback_data from buttons should be strings separated by the character "|"
    - Any data sent through callback_data cannot have the "|" for obvious reasons
    - Any callback_data should have at least one value
    - The first value in callback_data should be the kind of operation to deal
    - Be aware that the Update object has the user, chat and message information.
    
    example of callback_data:
    "vote|{vote_id}|{vote_option}"

    Where:
    - vote is a plain string indicating that the button came from an user voting
    - vote_id refers to the vote row/object in database to update.
    - vote_option should indicate if it was option A or B.

    A nice thing to do here if you are an SmallTalk expert is to make a parse
    the callback data and create classes that would handle those different cases.

"""


def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    callback_arguments = query.data.split("|")
    if callback_arguments[0] == "dame_botones":
        coso = callback_arguments[1]
        query.message.reply_text(f"apretaste algún botón y ahora se que sos un {coso}")
        try:
            query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        finally:
            pass


def te_doy_botones(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    callback_arguments = query.data.split("|")
    coso = callback_arguments[1]
    query.message.reply_text(f"apretaste algún botón y ahora se que sos un {coso}")
    try:
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    finally:
        pass
