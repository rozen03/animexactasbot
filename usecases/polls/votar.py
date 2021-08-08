import logging
from pony.orm import *  # pylint: disable=redefined-builtin
from models import Option, Vote, User

logger = logging.getLogger('animexactasbot.log')


@db_session
def get_options_from_poll(poll_id):
    poll_options = select(o for o in Option if o.poll.id == poll_id and o.approved)[:]
    return poll_options


@db_session
def create_vote(id_a, id_b, id_selected):
    generic_user = User(calls=1)
    Vote(option_a=Option[int(id_a)],
         option_b=Option[int(id_b)],
         user=generic_user,
         poll=Option[int(id_a)].poll,
         selected=int(id_selected))

    return Option[int(id_selected)].text
