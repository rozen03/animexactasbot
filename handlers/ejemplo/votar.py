#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import telegram

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import CallbackContext

from usecases.polls.votar import get_options_from_poll, create_vote
from handlers.utils.utils import obtener_botonera_polls


def votar(update: Update, context: CallbackContext):
    reply_markup = obtener_botonera_polls("votar_opciones")
    reply_msg = "Elija una de las siguientes encuestas a votar:"
    update.message.reply_text(reply_msg,
                              reply_markup=reply_markup)


def votar_opciones(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    callback_args = query.data.split("|")

    poll_name = callback_args[1]
    context.user_data['poll_id'] = callback_args[2]

    options = get_options_from_poll(callback_args[2])
    choices = random.sample(list(options), 2)

    if len(choices) == 2:
        choices_buttons = [
            InlineKeyboardButton(
                text=f"{choices[0].text}",
                callback_data=f"opcion_votada|{choices[0].id}|{choices[1].id}|{choices[0].id}"
            ),
            InlineKeyboardButton(
                text=f"{choices[1].text}",
                callback_data=f"opcion_votada|{choices[0].id}|{choices[1].id}|{choices[1].id}"
            )
        ]

        query.message.reply_text(
            f'Has elegido la encuesta de {poll_name}.\n\n'
            '¿Cuál de las siguientes opciones es la mejor?\n'
            f'[{choices[0].text}]({choices[0].url})\n'
            f'[{choices[1].text}]({choices[1].url})',
            reply_markup=InlineKeyboardMarkup([choices_buttons]),
            disable_web_page_preview=True,
            parse_mode=telegram.ParseMode.MARKDOWN
        )

        try:
            query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        finally:
            pass
    else:
        query.message.reply_text(
            f'Has elegido la encuesta de {poll_name}.\n\n'
            'No obstante, actualmente no hay 2 opciones para votar.'
            'Elija otra de las opciones.'
        )


def opcion_votada(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    callback_args = query.data.split("|")

    id_a, id_b, id_selected = (callback_args[1], callback_args[2], callback_args[3])

    selected_name = create_vote(id_a, id_b, id_selected)

    query.message.reply_text(f"Has votado {selected_name}. \n\n"
                             "Gracias por participar :D")

    try:
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    finally:
        pass
