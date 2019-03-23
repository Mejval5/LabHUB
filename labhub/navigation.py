#!/usr/bin/python
# -*- coding: utf

from flask_nav import Nav
from flask_nav.elements import Navbar, View


nav = Nav()

# nav.register_element(
#     "top_menu", Navbar(
#         View(u"Správce dat katastru", ".lvs"),
#         View(u"Katastry", ".land_registers"),
#         View(u"LV", ".lvs"),
#         View(u"Pozemky", ".estates"),
#         View(u"Vlastníci", ".owners"),
#         View(u"Stahováni", ".downloads"),
#         View(u"Scanování", ".scans"),
#         # View(u"Aktivity", ".activities"),
#         # View(u"Kalendář", ".calendar"),
#         View(u"Vytvořit uživatele", ".user_create"),
#         View(u"Odhlásit", ".logout"),
# 	    View(u"Reload", ".reload")
#     )
# )

nav.register_element(
    "top_menu", Navbar(
        View(u"Login", ".login")
    )
)