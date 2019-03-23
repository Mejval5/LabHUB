#!/usr/bin/python
# -*- coding: utf-8 -*-

from json import loads
from datetime import timedelta

from flask import Flask, session
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


from labhub.navigation import nav
from labhub.lib.database import Database

import psycopg2
import psycopg2.extensions
import sys
import re
import psycopg2
import requests
import logging

SESSIONLIFETIME = timedelta(minutes=60)
logging.basicConfig(filename='logs/error.log',level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = "ADSF168WT1ASDE58GAASRT8T4TSA6D5BV1ASWEFADSF8HYJYU8O"
app.permanent_session_lifetime = SESSIONLIFETIME

Bootstrap(app)
nav.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

with open("scihub/config.json") as conf_data:
    app.config.update(loads(conf_data.read()))

db = Database(**app.config["database"])

#scanner = Scanner(db)

import scihub.routes


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = SESSIONLIFETIME