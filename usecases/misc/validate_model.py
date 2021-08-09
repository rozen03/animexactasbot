#!/usr/bin/python3
# -*- coding: utf-8 -*-

from models import *  # pylint: disable=redefined-builtin


def get_model(button_type):
    for entity in db.Entity.__subclasses__():
        if entity.__name__ == button_type:
            return entity
    raise Exception(f"There is no class with {button_type} name")


@db_session
def validate_model(button_type, object_id):
    model = get_model(button_type)
    model[object_id].approved = True
