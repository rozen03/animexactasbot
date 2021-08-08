import logging
from pony.orm import *  # pylint: disable=redefined-builtin
from models import Option, Poll

logger = logging.getLogger('animexactasbot.log')


@db_session
def get_polls():
    polls = select(p for p in Poll if p.approved)[:]
    return polls


@db_session
def store_option(data):
    poll_id = data['poll_id']
    poll = Poll[poll_id]
    option = Option(
        poll=poll,
        text=data['nombre_opcion'],
        url=data['link']
    )
    return option
