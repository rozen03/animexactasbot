#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
# from pony.orm import *  # pylint: disable=redefined-builtin

from models import Poll, Vote, Option, Result, db_session, select, delete

logger = logging.getLogger('animexactasbot.log')


@db_session
def rank_poll(poll_id):
    votes = select(v for v in Vote if v.poll.id == poll_id)[:]
    scores = {o.id: 0 for o in select(o for o in Option if o.poll.id == poll_id)}
    for v in votes:
        if v.selected == 0:
            scores[v.option_a.id] += 1
        else:
            scores[v.option_b.id] += 1
    delete(r for r in Result if r.poll.id == poll_id)
    for option_id, score in scores.items():
        Result(poll=1, option=option_id, score=score)


def rank_polls():
    with db_session:
        poll_ids = select(p.id for p in Poll if p.delete_at is None)[:]

    for poll_id in poll_ids:
        rank_poll(poll_id=poll_id)
