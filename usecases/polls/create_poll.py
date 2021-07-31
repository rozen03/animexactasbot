from pony.orm import db_session
from models import Poll, Period


def create_poll_with_name(message_text):
    poll_name = message_text.split(" ", 1)[1]
    with db_session:
        Poll(text=poll_name, periodic_votes=2, period=Period.WEEKLY.name)
    return poll_name
