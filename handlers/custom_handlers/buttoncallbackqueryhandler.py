from telegram.ext import CallbackQueryHandler, Dispatcher
from telegram.ext.handler import UT, RT
from telegram.ext.utils.types import CCT
from telegram.ext.utils.promise import Promise
from typing import Union


class ButtonCallbackQueryHandler(CallbackQueryHandler):
    def handle_update(
        self,
        update: UT,
        dispatcher: 'Dispatcher',
        check_result: object,
        context: CCT = None,
    ) -> Union[RT, Promise]:
        query = update.callback_query
        callback_arguments = query.data.split("|")
        for i in range(1, len(callback_arguments)):
            context.user_data[f"button_reply_{i}"] = callback_arguments[i]

        return super().handle_update(
            update,
            dispatcher,
            check_result,
            context
        )
