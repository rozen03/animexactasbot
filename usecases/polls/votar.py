import logging
from pony.orm import *  # pylint: disable=redefined-builtin
from models import Option, Poll, Vote, User

logger = logging.getLogger('animexactasbot.log')


@db_session
def get_options_from_poll(poll_name):
    options = select(o for o in Option if o.poll.text == poll_name)[:]
    return options

@db_session
def create_vote(id_A, id_B, id_selected):
    u = User(calls=1)
    v = Vote(option_a=Option[int(id_A)],
        option_b=Option[int(id_B)],
        user=u,
        poll=Option[int(id_A)].poll,
        selected=int(id_selected))

    return Option[int(id_selected)].text