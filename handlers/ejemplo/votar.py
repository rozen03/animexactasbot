#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import random
import telegram

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import CallbackContext

from usecases.misc.user import save_user_from_button
from usecases.polls.ranking import rank_poll
from usecases.polls.sugerir_opcion import get_polls
from usecases.polls.votar import get_options_from_poll, create_vote
from handlers.utils.utils import obtener_botonera_polls


def deprecate_vote_message(context: CallbackContext):
    chat_id = context.job.context["chat_id"]
    message_id = context.job.context["message_id"]

    try:
        context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                              reply_markup=InlineKeyboardMarkup([]))
    finally:
        pass
    send_votation(context, None, None, None)


def votar(update: Update, context: CallbackContext):
    reply_markup = obtener_botonera_polls("votar_opciones")
    reply_msg = "Elija una de las siguientes encuestas a votar:"
    update.message.reply_text(reply_msg,
                              reply_markup=reply_markup)


def votar_opciones(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    callback_args = query.data.split("|")
    poll_name = callback_args[1]
    poll_id = callback_args[2]

    options = get_options_from_poll(poll_id)
    choices = random.sample(list(options), 2)

    if len(choices) == 2:
        send_votation(context, query, poll_id, poll_name)
    else:
        query.message.edit_text(
            f'Has elegido la encuesta de {poll_name}.\n\n'
            'No obstante, actualmente no hay 2 opciones para votar.'
            'Elija otra de las opciones.'
        )
    rank_poll(poll_id)


def opcion_votada(update: Update, context: CallbackContext) -> None:
    save_user_from_button(update, context)
    query = update.callback_query
    callback_args = query.data.split("|")

    id_a, id_b, id_selected = (callback_args[1], callback_args[2], callback_args[3])

    selected_name, voted = create_vote(id_a, id_b, id_selected, update.callback_query.from_user.id)
    if voted:
        context.bot.answer_callback_query(callback_query_id=query.id, text=f'votaste a {selected_name}',
                                          show_alert=True)
    else:
        context.bot.answer_callback_query(callback_query_id=query.id, text=f'Ya habías votado che', show_alert=True)


def send_votation(context: CallbackContext, query, poll_id, poll_name):
    if not poll_id:
        polls = get_polls()
        poll = random.choice(list(polls))
        poll_id = poll.id
        poll_name = poll.text
    options = get_options_from_poll(poll_id)
    choices = random.sample(list(options), 2)
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
    reroll = [InlineKeyboardButton(
        text="No sé, dame otro",
        callback_data=f"dame_otro|{poll_name}|{poll_id}"
    )]
    reply_markup = InlineKeyboardMarkup([choices_buttons, reroll])
    try:
        chat_id = query.message.chat_id
        message_id = query.message.message_id
        message_text = query.message.text
        query.edit_message_text(
            f'Has elegido la encuesta de {poll_name}.\n\n'
            '¿Cuál de las siguientes opciones es la mejor?\n'
            f'[{choices[0].text}]({choices[0].url})\n'
            f'[{choices[1].text}]({choices[1].url})',
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
    except Exception as e:
        print("send_votation error", e)
        print(context.job.context)
        return
        chat_id = context.job.context["chat_id"]
        message = context.bot.send_message(text=f'Has elegido la encuesta de {poll_name}.\n\n'
                                                '¿Cuál de las siguientes opciones es la mejor?\n'
                                                f'[{choices[0].text}]({choices[0].url})\n'
                                                f'[{choices[1].text}]({choices[1].url})',
                                           chat_id=chat_id,
                                           reply_markup=reply_markup,
                                           disable_web_page_preview=True,
                                           parse_mode=telegram.ParseMode.MARKDOWN)

        message_id = message.message_id
        message_text = message.text
    finally:
        pass
    new_context = dict()
    new_context["message_id"] = message_id
    new_context["message_text"] = message_text
    new_context["chat_id"] = chat_id

#    context.job_queue.run_once(deprecate_vote_message, datetime.timedelta(hours=4), context=new_context)


def send_random_votes(context: CallbackContext, chat_id: str):
    polls = get_polls()
    poll = random.choice(list(polls))
    poll_id = poll.id
    poll_name = poll.text
    options = get_options_from_poll(poll_id)
    choices = random.sample(list(options), 2)
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
    reroll = [InlineKeyboardButton(
        text="No sé, dame otro",
        callback_data=f"dame_otro|{poll_name}|{poll_id}"
    )]
    reply_markup = InlineKeyboardMarkup([choices_buttons, reroll])
    message = context.bot.send_message(text=f'Votemos la encuesta de {poll_name}.\n\n'
                                            '¿Cuál de las siguientes opciones es la mejor?\n'
                                            f'[{choices[0].text}]({choices[0].url})\n'
                                            f'[{choices[1].text}]({choices[1].url})',
                                       chat_id=chat_id,
                                       reply_markup=reply_markup,
                                       disable_web_page_preview=True,
                                       parse_mode=telegram.ParseMode.MARKDOWN)