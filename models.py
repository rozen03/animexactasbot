#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
from enum import Enum, auto

from pony.orm import *  # pylint: disable=redefined-builtin

db = Database()


class Period(Enum):  # pylint: disable=missing-class-docstring
    WEEKLY = auto()
    MONTHLY = auto()


class Poll(db.Entity):  # pylint: disable=missing-class-docstring
    text = Required(str)
    created_at = Required(datetime.datetime, default=datetime.datetime.utcnow)
    delete_at = Optional(datetime.datetime)
    periodic_votes = Required(int)
    period = Required(str)
    results = Optional("Results")
    options = Set("Option")


class Option(db.Entity):  # pylint: disable=missing-class-docstring
    text = Required(str)
    url = Required(str)
    created_at = Required(datetime.datetime, default=datetime.datetime.utcnow)
    vote_a = Optional("Vote", reverse="option_a")
    vote_b = Optional("Vote", reverse="option_b")
    results = Optional("Results")
    approved = Required(bool, default=False)
    poll = Required("Poll")


class Vote(db.Entity):  # pylint: disable=missing-class-docstring
    created_at = Required(datetime.datetime, default=datetime.datetime.utcnow)
    option_a = Required("Option")
    option_b = Required("Option")
    user = Required("User")
    selected = Required(int)


class Results(db.Entity):  # pylint: disable=missing-class-docstring
    poll = Required("Poll")
    option = Required("Option")
    order = Required(int)
    score = Optional(float)


class User(db.Entity):  # pylint: disable=missing-class-docstring
    last_draw = Required(datetime.datetime, default=datetime.datetime.now())
    first_name = Optional(str)
    last_name = Optional(str)
    username = Optional(str)
    calls = Required(int, default=1)
    votes = Optional("Vote")


# noinspection Pylint
def init_db(path):
    db.bind('sqlite', path, create_db=True)
    db.generate_mapping(create_tables=True)
