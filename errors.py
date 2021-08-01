# -*- coding: utf-8 -*-

import logging

from telegram import (Update)
from telegram.ext import (CallbackContext)

logger = logging.getLogger("animexactasbot.log")


def error_callback(update: Update, context: CallbackContext):
    logger.exception(context.error)
    # Spammeo a rozen con los bugazos
    context.bot.sendMessage(137497264, text=str(context.error))
    context.bot.sendMessage(137497264, text=str(update))
