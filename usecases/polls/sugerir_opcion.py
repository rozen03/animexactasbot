from pony.orm import *
from models import Option, Poll

def polls():
    polls = select(p for p in Poll)
    return polls

def storeOption(data):
    poll_id = data['poll_id']
    poll = Poll[poll_id]

    option = Option(
        poll=poll,
        text=data['nombre_opcion'],
        url=data['link']
    )
    