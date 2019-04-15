#!/usr/bin/python
# -*- coding: utf-8 -*-

from wtforms import Form
from wtforms import IntegerField, TextField, PasswordField, DateTimeField, BooleanField, TextAreaField
from wtforms.widgets import HiddenInput
from wtforms.validators import NumberRange, DataRequired, Length, Optional

class LrManipulateForm(Form):
    """
    Class validating all lr operations (adding to/moving in/deleting from queue etc.)
    """
    lr_number = IntegerField("lr_number", [DataRequired(), NumberRange(min=0)], widget=HiddenInput())


class LoginForm(Form):
    """
    Class validating login of user.
    """
    username = TextField("username", [DataRequired(), Length(max=42)])
    password = PasswordField("password", [DataRequired()])


class CreateUserForm(Form):
    """
    Class validating creation of new user.
    """
    login = TextField("login", [DataRequired(), Length(max=42)])
    name = TextField("name", [Length(max=64)])
    mail = TextField("mail", [DataRequired(), Length(min=6, max=64)])
    password = PasswordField("password", [DataRequired(), Length(min=5, max=64)])
    password_check = PasswordField("password_check", [DataRequired(), Length(min=5, max=64)])


