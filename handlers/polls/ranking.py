#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (Update)
from telegram.ext import (CallbackContext)

from handlers.utils.utils import obtener_botonera_polls
from usecases.polls.ranking import get_rank
from usecases.polls.ranking import rank_polls


def command_rank_polls(update: Update, context: CallbackContext):
    rank_polls()


def job_rank_polls(context: CallbackContext):
    rank_polls()


def get_ranking_polls(update: Update, context: CallbackContext):
    reply_markup = obtener_botonera_polls("get_ranking")
    update.message.reply_text(
        "De que poll querés ver el ranking?",
        reply_markup=reply_markup,
    )


def get_ranking(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    callback_args = query.data.split("|")

    poll_name = callback_args[1]
    poll_id = callback_args[2]

    ranks = get_rank(poll_id)
    ranks_text = str.join("\n", [f"{k + 1}.{name}" for k, name in enumerate(ranks)])

    try:
        query.edit_message_text(text=f'Elegiste el poll de {poll_name}.\n\n' + ranks_text)
    finally:
        pass
