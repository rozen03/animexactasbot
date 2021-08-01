from telegram import Update
from telegram.ext import CallbackContext

from usecases.misc import dale_dante


def reply_dale_dante(update: Update, context: CallbackContext):
    bio = dale_dante.create_dale_dante()
    update.message.reply_photo(
        photo=bio,
        caption="Dale dante!",
        quote=False
    )
