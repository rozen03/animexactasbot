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
    for vote in votes:
        if vote.selected == 0:
            scores[vote.option_a.id] += 1
        else:
            scores[vote.option_b.id] += 1
    delete(r for r in Result if r.poll.id == poll_id)
    for option_id, score in scores.items():
        Result(poll=1, option=option_id, score=score)


def rank_polls():
    with db_session:
        poll_ids = select(p.id for p in Poll if p.delete_at is None)[:]

    for poll_id in poll_ids:
        rank_poll(poll_id=poll_id)
"""
>>> from rankit.Table import *
>>> from rankit.Ranker import *

>>> matrez=[[0,1,0,1],[0,2,0,1],[2,1,1,0]]
>>> pd.DataFrame(matrez, columns=["team_a","team_b","result_a","result_b"])
   team_a  team_b  result_a  result_b
0       0       1         0         1
1       0       2         0         1
2       2       1         1         0
>>> df=pd.DataFrame(matrez, columns=["team_a","team_b","result_a","result_b"])
>>> Tab
TabError(  Table(     
>>> Table(df, col=["team_a","team_b","result_a","result_b"])
Table with provided data:
   host  visit  hscore  vscore
0     0      1       0       1
1     0      2       0       1
2     2      1       1       0
>>> table=Table(df, col=["team_a","team_b","result_a","result_b"])
>>> coco=ColleyRanker()
>>> coco.rank(table)
   name  rating  rank
0     2     0.7     1
1     1     0.5     2
2     0     0.3     3

"""