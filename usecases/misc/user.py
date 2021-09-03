from pony.orm import db_session, commit
from telegram import Update
from telegram.ext import CallbackContext

from models import User


def save_user_from_message(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    return save_user(tg_user)


def save_user_from_button(update: Update, context: CallbackContext):
    tg_user = update.callback_query.from_user
    return save_user(tg_user)


def save_user(tg_user):
    user_id = tg_user.id
    first_name = tg_user.first_name
    last_name = tg_user.last_name if tg_user.last_name else ""
    username = tg_user.username if tg_user.username else ""
    with db_session:
        user = User.get_for_update(id=user_id)
        if not user:
            user = User(id=user_id,
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        )
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.calls = user.calls + 1
        commit()
        return user
