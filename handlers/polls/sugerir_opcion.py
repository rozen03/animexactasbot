import logging

from telegram import (
    Update,
    InlineKeyboardMarkup
)
from telegram.ext import CallbackContext, ConversationHandler

from handlers.utils.utils import obtener_botonera_polls
from handlers.utils.valide_suggestion import create_suggestion_validation
from usecases.polls.sugerir_opcion import store_option

NOMBRE, LINK = range(2)

logger = logging.getLogger('animexactasbot.log')


def polls_reply(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    callback_args = query.data.split("|")

    poll_name = callback_args[1]
    context.user_data['poll_id'] = callback_args[2]

    query.message.reply_text(
        f'Elegiste el poll de {poll_name}.\n\n'
        '¿Cuál es el nombre de la sugerencia?'
    )

    try:
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    finally:
        pass


def sugerir_opcion(update: Update, context: CallbackContext):
    reply_markup = obtener_botonera_polls("polls_reply")
    update.message.reply_text(
        "De que poll querés sugerir una opción?\n\n"
        "Si querés cancelar la operación, podes escribir el comando /cancelar",
        reply_markup=reply_markup
    )
    return NOMBRE


def nombre(update: Update, context: CallbackContext) -> int:
    context.user_data["nombre_opcion"] = update.message.text

    update.message.reply_text(
        "Genial! Ahora pasame un link (Youtube, Vimeo, MAL, IMDb, etc)."
    )

    return LINK


def link(update: Update, context: CallbackContext) -> int:
    context.user_data['link'] = update.message.text

    option = store_option(context.user_data)

    reply_markup = create_suggestion_validation(option.__class__.__name__, option.id)
    context.bot.sendMessage(chat_id=137497264,
                            text=f"{option.__class__.__name__}: {option.text}\n {option.url}",
                            reply_markup=reply_markup)
    # noinspection Pylint
    update.message.reply_text(
        # noinspection Pylint
        """Tu sugerencia fue añadida al poll correctamente.
        Cuando sea aceptada aparecerá entre las opciones a rankear.
        
        Felicitaciones Dante!!"""
    )

    return ConversationHandler.END


def cancelar(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Cancelaste la operación.\n\n"
        "Volvé a ingresar un comando para iniciar una nueva operación."
    )

    return ConversationHandler.END
