#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

import pandas as pd
from pony.orm import desc
from rankit import Ranker
from rankit.Table import Table
from models import Poll, Vote, Option, Result, db_session, select, delete
from usecases.polls.my_ranker import MyColleyRanker

logger = logging.getLogger('animexactasbot.log')

ranker = MyColleyRanker()


# ranker = Ranker.KeenerRanker()


@db_session
def rank_poll(poll_id):
    votes = select(v for v in Vote if v.poll.id == poll_id and v.poll.approved)[:]
    used = {o.id: False for o in select(o for o in Option if o.poll.id == poll_id and o.approved)}
    votes_matrix = []
    for vote in votes:
        opta = vote.option_a.id
        optb = vote.option_b.id
        if vote.selected == opta:
            row = [opta, optb, 1, 0]
        elif vote.selected == optb:
            row = [opta, optb, 0, 1]
        else:
            raise Exception("QUE PASO POR Q HAY UNA OPCION NUEVA???")
        used[opta] = True
        used[optb] = True
        votes_matrix.append(row)
    for key, value in used.items():
        if not value:
            votes_matrix.append([key, key, 0, 0])  # ah, i'm drinking falop again

    data_frame = pd.DataFrame(votes_matrix, columns=["team_a", "team_b", "result_a", "result_b"])
    table = Table(data_frame, col=["team_a", "team_b", "result_a", "result_b"])
    ranking = ranker.rank(table)
    delete(r for r in Result if r.poll.id == poll_id)
    for index, row in ranking.iterrows():
        Result(poll=poll_id, option=int(row["name"]), score=row["rating"])


def rank_polls():
    with db_session:
        poll_ids = select(p.id for p in Poll if p.delete_at is None and p.approved)[:]

    for poll_id in poll_ids:
        rank_poll(poll_id=poll_id)

@db_session
def get_rank(poll_id):
    rankings = select(r for r in Result if r.poll.id == poll_id).order_by(desc(Result.score))
    response = [r.option.text for r in rankings]
    return response
