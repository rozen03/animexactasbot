#!/usr/bin/python3
# -*- coding: utf-8 -*-
import inspect
import sys

from models import *  # pylint: disable=redefined-builtin


def get_model(button_type):
    for name, obj in inspect.getmembers(sys.modules["models"]):
        if inspect.isclass(obj) and name == button_type:
            return obj
    raise Exception(f"There is no class with {button_type} name")


@db_session
def validate_model(button_type, object_id):
    model = get_model(button_type)
    model[object_id].approved = True
