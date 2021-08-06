#!/usr/bin/python3
# -*- coding: utf-8 -*-
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from usecases.polls.sugerir_opcion import get_polls

def aux_create_option_button(cb_name, poll):
    return InlineKeyboardButton(
        text=f"{poll.text}",
        callback_data=f"{cb_name}|{poll.text}|{poll.id}"
    )

def obtener_botonera_polls(callback_name):
    polls = get_polls()
    columns = 3
    botones = []
    for k in range(0, len(polls), columns):
        # TODO: make a function out of this
        row = [aux_create_option_button(callback_name, p) for p in polls[k:k + columns]]
        botones.append(row)
    reply_markup = InlineKeyboardMarkup(botones)
    return reply_markup