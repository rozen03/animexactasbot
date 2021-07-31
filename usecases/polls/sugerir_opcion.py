import logging
from pony.orm import *
from models import Option, Poll

logger = logging.getLogger('animexactasbot.log')


@db_session
def get_polls():
    polls = select(p for p in Poll)[:]
    return polls


@db_session
def store_option(data):
    poll_id = data['poll_id']
    poll = Poll[poll_id]

    # En esta primera version, tomaremos como aprobados todas las sugerencias

    # TODO: implementar un comando para aprobar o desechar sugerencias falopa que no formen parte del poll... o pornetas.

    option = Option(
        poll=poll,
        text=data['nombre_opcion'],
        url=data['link'],
        approved=True
    )
