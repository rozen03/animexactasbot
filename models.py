#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pony.orm import *
from enum import Enum, auto
import datetime

db = Database()


class Period(Enum):
    DAILY = auto()
    WEEKLY = auto()
    MONTHLY = auto()


class Poll(db.Entity):
    text = Required(str)
    created_at = Required(datetime.datetime, default=datetime.datetime.utcnow)
    delete_at = Optional(datetime.datetime)
    periodic_votes = Required(int)
    period = Required(str)
    results = Optional("Results")
    options = Set("Option")


class Option(db.Entity):
    text = Required(str)
    url = Required(str)
    created_at = Required(datetime.datetime, default=datetime.datetime.utcnow)
    vote_a = Optional("Vote", reverse="option_a")
    vote_b = Optional("Vote", reverse="option_b")
    results = Optional("Results")
    approved = Required(bool, default=False)
    poll = Required("Poll")


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
    votes = Optional("Vote")


def init_db(path):
    db.bind('sqlite', path, create_db=True)
    db.generate_mapping(create_tables=True)
