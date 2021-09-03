import logging
import threading

from pony.orm import *  # pylint: disable=redefined-builtin
from models import Option, Vote, User

logger = logging.getLogger('animexactasbot.log')

# Python create mutex
votes_mutex = threading.Lock()


@db_session
def get_options_from_poll(poll_id):
    poll_options = select(o for o in Option if o.poll.id == poll_id and o.approved)[:]
    return poll_options


@db_session
def create_vote(id_a, id_b, id_selected, user_id):
    user = User[user_id]
    option_a = Option[int(id_a)]
    option_b = Option[int(id_b)]
    with votes_mutex:
        vote = select(v for v in Vote if v.user == user and v.option_a == option_a and v.option_b == option_b).limit(1)[
               :]
        if len(vote) > 0:
            return "", False
        Vote(option_a=Option[int(id_a)],
             option_b=Option[int(id_b)],
             user=user,
             poll=Option[int(id_a)].poll,
             selected=int(id_selected))

    return Option[int(id_selected)].text, True
