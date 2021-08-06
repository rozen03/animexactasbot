#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (Update)
from telegram.ext import (CallbackContext,CommandHandler)

from usecases.polls.ranking import rank_polls

from handlers.basehandler import BaseHandler


class RankingHandler(BaseHandler):
    """Implement handlers for poll creation"""
    @staticmethod
    def build_handler():
        return CommandHandler('rankeameloh', command_rank_polls, run_async=True)


    @staticmethod
    def has_description():
        return False

    @staticmethod
    def command_name():
        pass

    @staticmethod
    def command_description():
        pass
    

def command_rank_polls(update: Update, context: CallbackContext):
    rank_polls()


def job_rank_polls(context: CallbackContext):
    rank_polls()
