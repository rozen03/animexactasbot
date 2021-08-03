#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (Update)
from telegram.ext import (CallbackContext)

from usecases.polls.ranking import rank_polls


def command_rank_polls(update: Update, context: CallbackContext):
    rank_polls()


def job_rank_polls(context: CallbackContext):
    rank_polls()
