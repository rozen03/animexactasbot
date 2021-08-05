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
    results = Set("Result")
    options = Set("Option")
    votes = Set("Vote")


class Option(db.Entity):  # pylint: disable=missing-class-docstring
    text = Required(str)
    url = Required(str)
    created_at = Required(datetime.datetime, default=datetime.datetime.utcnow)
    vote_a = Set("Vote", reverse="option_a")
    vote_b = Set("Vote", reverse="option_b")
    results = Optional("Result")
    approved = Required(bool, default=False)
    poll = Required("Poll")


class Vote(db.Entity):  # pylint: disable=missing-class-docstring
    created_at = Required(datetime.datetime, default=datetime.datetime.utcnow)
    option_a = Required("Option")
    option_b = Required("Option")
    user = Required("User")
    poll = Required("Poll")
    selected = Required(int)


class Result(db.Entity):  # pylint: disable=missing-class-docstring
    poll = Required("Poll")
    option = Required("Option")
    score = Optional(float)


class User(db.Entity):  # pylint: disable=missing-class-docstring
    first_name = Optional(str)
    last_name = Optional(str)
    username = Optional(str)
    calls = Required(int, default=1)
    votes = Set("Vote")


def init_db(path):
    db.bind('sqlite', path, create_db=True)
    db.generate_mapping(create_tables=True)


def init_clear_db(path):
    db.bind('sqlite', path, create_db=True)
    db.generate_mapping(create_tables=True)
    set_sql_debug(True)
    db.drop_all_tables(with_all_data=True)
    db.create_tables()
