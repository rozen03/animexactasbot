#!/usr/bin/python3
# -*- coding: utf-8 -*-
from models import Poll, Option, User, Vote, db_session, init_clear_db, Period, commit

init_clear_db("animexactasbot.sqlite3")

with db_session:
    poll = Poll(text="Prueba", periodic_votes=2, period=Period.WEEKLY.name)
    user = User(first_name="pepe")
    for i in range(10):
        Option(poll=poll, text=f"opcion {i}", url="https://www.google.com", approved=True)
    commit()
    voto_a = Vote(option_a=Option[1], option_b=Option[2], selected=0, poll=poll, user=user)
    commit()
    voto_b = Vote(option_a=Option[3], option_b=Option[2], selected=1, poll=poll, user=user)
    commit()
    voto_c = Vote(option_a=Option[3], option_b=Option[4], selected=0, poll=poll, user=user)
    commit()
    voto_d = Vote(option_a=Option[1], option_b=Option[4], selected=0, poll=poll, user=user)
    commit()
    voto_e = Vote(option_a=Option[5], option_b=Option[4], selected=1, poll=poll, user=user)
    commit()
