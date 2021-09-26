from pony.orm import set_sql_debug

from models import Option, db_session, select


@db_session
def list_poll_options(poll_id):
    option_list = select((o.text, o.url, o.id) for o in Option if o.poll.id == poll_id).order_by(lambda: o.text)[:]
    return option_list
