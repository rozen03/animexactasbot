#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pony.orm import *
import datetime

db = Database()


class Poll(db.Entity):
    text = Required(str)
    created_at = Required(datetime.datetime, default=datetime.datetime.utcnow)
    delete_at = Required(datetime.datetime)
    periodic_votes = Required(int)
    period = Required(str)


class Option(db.Entity):
    text = Required(str)
    url = Required(str)
    created_at = Required(datetime.datetime, default=datetime.datetime.utcnow)

class Vote(db.Entity):
    created_at = Required(datetime.datetime, default=datetime.datetime.utcnow)
    option_a = Required("Option")
    option_b = Required("Option")
    user = Required("User")
    selected = Required(int)


class Results(db.Entity):
    poll = Required("Poll")
    option = Required("Option")
    order = Required(int)
    score = Optional(float)


class User(db.Entity):
    last_draw = Required(datetime.datetime, default=datetime.datetime.now())
    first_name = Optional(str)
    last_name = Optional(str)
    username = Optional(str)
    calls = Required(int, default=1)
    # cards = Set(lambda: Card, reverse='users')
    # suggested_cards = Set(lambda: Card, reverse='suggester')


def init_db(path):
    db.bind('sqlite', path, create_db=True)
    db.generate_mapping(create_tables=True)