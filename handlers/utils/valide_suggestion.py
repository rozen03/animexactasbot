#!/usr/bin/python3
# -*- coding: utf-8 -*-
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


def boton(text, data):
    return InlineKeyboardButton(text=text, callback_data=data)


def create_suggestion_validation(cb_type, object_id) -> InlineKeyboardMarkup:
    aceptar = boton(text="Aceptar", data=f"validate_button|{cb_type}|{object_id}|0")
    rechazar = boton(text="Rechazar", data=f"validate_button|{cb_type}|{object_id}|1")
    botones = [aceptar, rechazar]
    return InlineKeyboardMarkup([botones])
