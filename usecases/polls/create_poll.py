from pony.orm import db_session
from models import Poll, Period


def create_poll_with_name(poll_name) -> None:
    with db_session:
        Poll(text=poll_name, periodic_votes=2, period=Period.WEEKLY.name)
