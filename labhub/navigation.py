#!/usr/bin/python
# -*- coding: utf

from flask_nav import Nav
from flask_nav.elements import Navbar, View


nav = Nav()

nav.register_element(
    "top_menu", Navbar(
        View(u"Home", ".index"), 
        View(u"Login", ".login")
    )
)