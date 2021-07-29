from pony.orm import db_session
from models import Poll
from enum import Enum, auto


class Period(Enum):
    DAILY=auto()
    WEEKLY=auto()
    MONTHLY=auto()

def create_poll_with_name(message_text):
    poll_name=(message_text).split(" ", 1)[1]
    with db_session:
        poll=Poll(text=poll_name,periodic_votes=2,period=Period.WEEKLY.name)
    return poll_name