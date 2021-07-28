#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram import (ChatAction, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, Update, constants)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler, Updater)
logger = logging.getLogger("animexactasbot.log")
def error_callback(update: Update, context: CallbackContext):
    logger.exception(context.error)
    #Spammeo a rozen con los bugazos
    context.bot.sendMessage(137497264, text=str(context.error))
    context.bot.sendMessage(137497264, text=str(update))
