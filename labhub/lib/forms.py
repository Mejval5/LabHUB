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


class EditActivityForm(Form):
    """
    Class validating creation or edit of activity
    """
    channel = TextField("channel", [Length(max=32)])
    date = DateTimeField("date", [DataRequired()], format='%Y-%m-%d')
    result = TextField("result")
    note = TextAreaField("note")
    owner = IntegerField("owner", [DataRequired(), NumberRange(min=0)], widget=HiddenInput())
    act_id = IntegerField("act_id", [NumberRange(min=0), Optional()], widget=HiddenInput())


class DeleteActivityForm(Form):
    """
    Class validating deleting of activity.
    """
    owner = IntegerField("owner", [DataRequired(), NumberRange(min=0)], widget=HiddenInput())
    act_id = IntegerField("act_id", [NumberRange(min=0), DataRequired()], widget=HiddenInput())


class ScannerAddForm(Form):
    """
    Class validating scanner item.
    """
    lr_name = TextField("lr_name", [DataRequired()])
    lr_id = IntegerField("lr_id", [NumberRange(min=0), DataRequired()])
    force = TextField("force", [DataRequired()], widget=HiddenInput())

class OwnerEditForm(Form):
    """
    Class validating owner edit.
    """
    owner_id = IntegerField("owner_id", [NumberRange(min=0), DataRequired()])
    mail = TextField("mail")
    phone = TextField("phone")
    city = TextField("city")
    street = TextField("street")
    str_number = TextField("str_number")
    post_code = TextField("post_code")
    birth = TextField("birth")

class OwnerNoteForm(Form):
    """
    Class validating note edit.
    """
    owner = IntegerField("owner", [NumberRange(min=0), DataRequired()], widget=HiddenInput())
    note = TextField("note", [DataRequired()])

class OwnerTagForm(Form):
    """
    Class validating owner tag saving.
    """
    owner = IntegerField("owner", [NumberRange(min=0), DataRequired()], widget=HiddenInput())
    tag_negotiation = BooleanField("tag_negotiation")
    tag_success = BooleanField("tag_success")
    tag_failure = BooleanField("tag_failure")
    tag_execution = BooleanField("tag_execution")
    tag_call = BooleanField("tag_call")
    tag_change = BooleanField("tag_change")
    tag_find_owners = BooleanField("tag_find_owners")
    tag_call_later = BooleanField("tag_call_later")
    tag_call_not = BooleanField("tag_call_not")
    tag_oslovit = BooleanField("tag_oslovit")

class AddVideo(Form):
    """
    Class validating creation of new user.
    """
    name = TextField("name", [Length(max=64)])
    link = TextField("link", [DataRequired(), Length(min=1, max=64)])

class DownloadOne(Form):
    """
    Class validating creation of new user.
    """
    lr_name = TextField("lr_name",)  
    lr_id = IntegerField("lr_id", [NumberRange(min=0), DataRequired()])
    lv_id = IntegerField("lv_id", [NumberRange(min=0), DataRequired()])
