#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import copy
from flask import render_template, redirect, url_for, request, flash
from flask_paginate import Pagination
from flask_login import login_user, logout_user, login_required, current_user

from labhub import app, db

from labhub.lib.forms import LrManipulateForm, LoginForm, CreateUserForm, EditActivityForm, DeleteActivityForm, ScannerAddForm, OwnerEditForm, OwnerNoteForm, OwnerTagForm, AddVideo, DownloadOne
from labhub.lib.pagination import Pagination

from labhub.user import User

import pandas as pd
import unicodecsv as csv
from io import BytesIO

def _default_params(args):
    """
    Suport function for parsing order and page args.
    """
    return {
        "order_by": args.get("order_by", "").lower(),
        "order_dir": args.get("order_dir", "asc").lower(),
        "page": args.get("page", 1) if not bool(args.get("filtered")) else 1,
        "per_page": args.get("per_page", 30),
    }

@app.route("/")
@app.route("/index/")
def index():
    return redirect(url_for("login"))

##################
# routes with view
##################

@app.route("/login/", methods=["GET", "POST"])
def login():
    # send logged user away
    if current_user.is_authenticated:
        return redirect(url_for("login"))

    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        user = User(form.username.data, db)

        if user.verify(form.password.data):
            login_user(user)
            return redirect(url_for("login"))

        else:
            flash(u"Špatná kombinace jména a hesla.", "error")
            return redirect(url_for("login"))

    else:
        return render_template("login.html")


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/forgotten_password")
def forgotten_password():
    # parse post
    return render_template("forgotten_password.html")


@app.route("/users/")
def users():
    return render_template("users.html", guu=u"lol")


# @app.route("/user_detail/")
# @login_required
# def user_detail():
#     return render_template("user_detail.html")


# @app.route("/downloads/", methods=["GET", "POST"])
# @login_required
# def downloads():
#     lr = Download(db)

#     form = DownloadOne(request.form)

#     if request.method == "POST" and form.validate():

#         land = LandRegister(db)
#         register = land.get(form.lr_id.data)
#         res=None
        
#         # validate and create new lr
#         if not register:
#             res = land.create(form.lr_id.data, form.lr_name.data.encode('utf-8'))

#             if not res:
#                 msg = u"nepodařilo se vytvořt zadaný katastr"

#         if res or register:
#             LvDownloader(form.lr_id.data).add_one(form.lv_id.data)
#         else:
#             flash(u"Katastr se nepodařilo přidat - "+msg, "error")

#         downloader.add_to_queue(form.lr_id.data)
#         return render_template("downloads.html",
#         downloaded=True,
#         lr=form.lr_id.data,
#         lr_number=form.lr_id.data,
#         lv=form.lv_id.data,
#         current=lr.get_bar(),
#         queue=lr.list_queue())

#     else:
#         return render_template("downloads.html",
#         current=lr.get_bar(),
#         queue=lr.list_queue())

    
#     return render_template(
#         "downloads.html",
#         current=lr.get_bar(),
#         queue=lr.list_queue()
#     )


# @app.route("/scans/")
# @login_required
# def scans():
#     scan = Scan(db)

#     return render_template(
#         "scans.html",
#         current=scan.get_bar(),
#         queue=scan.list_queue()
#     )


# @app.route("/scans_add/")
# @login_required
# def scans_add():
#     return render_template("scans_add.html")


# @app.route("/land_registers/")
# @login_required
# def land_registers():
#     params = _default_params(request.args)
#     params["filters"] = {
#         "completeness": request.args.get("completeness", "all"),
#         "locality": request.args.get("locality")
#     }

#     lr = LandRegister(db)

#     reg = params["filters"]["locality"]
#     if reg:
#         lr_number = lr.get_number(params["filters"]["locality"])

#         if lr_number is None:
#             flash(u"Nepodařilo se určit katastr.", "warning")

#         params["filters"]["reg_number"] = lr_number


#     data = lr.list(**params)

#     pagination = Pagination(
#         params["page"],
#         params["per_page"],
#         lr.count(params["filters"])
#     )

#     # ugly hack - "locality" cannot be legal filter for land register, so it is deleted
#     #               while processing filters, but needs to be present again for web
#     params["filters"]["locality"] = reg

#     return render_template(
#         "land_registers.html",
#         pagination=pagination,
#         data=data,
#         **params
#     )


# @app.route("/owners/")
# @login_required
# def owners():
#     params = _default_params(request.args)
#     params["filters"] = {
#         "name": request.args.get("name"),
#         "lv_number": request.args.get("lv_number"),
#         "expanse": request.args.get("expanse", "all"),
#         "active": request.args.get("active", "all"),
#         "land_register": request.args.get("land_register"),
#         "city": request.args.get("city"),
#         "tag": request.args.get("tag"),
#         "excel": request.args.get("excel")
#     }

#     lr = params["filters"]["land_register"]
#     if lr:
#         lr_number = LandRegister(db).get_number(params["filters"]["land_register"])

#         if lr_number is None:
#             flash(u"Nepodařilo se určit katastr.", "warning")

#         params["filters"]["lr_number"] = lr_number
    
#     ex = params["filters"]["excel"]
#     owner = Owner(db)
#     data = owner.list(**params)

#     excel_data = data
#     keys = excel_data[0].keys()
    
#     df = pd.DataFrame(data=list(excel_data), columns=keys)
#     if ex:
#         with open('data.csv', 'wb') as output_file:
#             for i in xrange(len(data)):
#                 dict_writer = csv.writer(output_file, encoding='utf-8')
#                 dict_writer.writerows(data[i])   
#     pagination = Pagination(
#         params["page"],
#         params["per_page"],
#         owner.count(params["filters"])
#     )

#     # ugly hack - "land_register" cannot be legal filter for owner, so it is deleted
#     #               while processing filters, but needs to be present again for web
#     params["filters"]["land_register"] = lr

#     return render_template(
#         "owners.html",
#         pagination=pagination,
#         data=data,
#         **params
#     )


# @app.route("/owner_detail/<int:owner_id>")
# @login_required
# def owner_detail(owner_id=None):
#     owner = Owner(db)

#     if owner.exists(owner_id):
#         return render_template(
#             "owner_detail.html",
#             owner=owner.get(owner_id),
#             activities=owner.getActivities(owner_id),
#             pastActivities=owner.getActivities(owner_id, past=True)
#         )
#     else:
#         return render_template("owner_not_found.html")


# @app.route("/owner_edit/<int:owner_id>")
# @login_required
# def owner_edit(owner_id=None):
#     owner = Owner(db)

#     if owner.exists(owner_id):
#         return render_template(
#             "owner_edit.html",
#             owner=owner.get(owner_id)
#         )
#     else:
#         return render_template("owner_not_found.html")


# @app.route("/lvs/")
# @login_required
# def lvs():
#     params = _default_params(request.args)
#     params["filters"] = {
#         "locality": request.args.get("locality"),
#         "lr_number": request.args.get("lr_number"),
#         "downloaded": request.args.get("downloaded", "true"),
#         "owner": request.args.get("owner"),
#         "expanse": request.args.get("expanse", "all")
#     }

#     lv = Lv(db)
#     data = lv.list(**params)
#     owner = Owner(db)
#     own = params["filters"]["owner"]
#     tru = False
#     if own:
#         tru = own.isdigit()
#         if tru:
#             own=owner.get(own)

#     pagination = Pagination(
#         params["page"],
#         params["per_page"],
#         lv.count(params["filters"])
#     )

#     # add lr_number if not given
#     if not params["filters"]["lr_number"]:
#         lr = LandRegister(db)
#         params["filters"]["lr_number"] = lr.get_number(params["filters"]["locality"])
#     #add locality if not given
#     if not params["filters"]["locality"]:
#         lr = LandRegister(db)
#         params["filters"]["locality"] = lr.get_locality(params["filters"]["lr_number"])

#     return render_template(
#         "lvs.html",
#         pagination=pagination,
#         locality=params["filters"]["locality"],
#         owner=params["filters"]["owner"],
#     owner_all=own,
#         data=data,
#         tru=tru,
#         **params
#     )


# @app.route("/estates/")
# @login_required
# def estates():
#     params = _default_params(request.args)
#     params["filters"] = {
#         "locality": request.args.get("locality"),
#         "lv_number": request.args.get("lv_number"),
#         "owner": request.args.get("owner"),
#         "type": request.args.get("type", "all"),
#         "expanse": request.args.get("expanse", "all")
#     }

#     est = Estate(db)
#     data = est.list(**params)
#     owner = Owner(db)
#     own = params["filters"]["owner"]
#     tru = False
#     if own:
#         tru = own.isdigit()
#         if tru:
#             own=owner.get(own)

#     pagination = Pagination(
#         params["page"],
#         params["per_page"],
#         est.count(params["filters"])
#     )

#     return render_template(
#         "estates.html",
#         pagination=pagination,
#         types=est.get_types(),
#         data=data,
#     owner=own,
#         tru=tru,
#         **params
#     )


# @app.route("/activities/")
# @login_required
# def activities():
#     return render_template("activities.html")


# @app.route("/activity_add/")
# @login_required
# def activity_add():
#     owner = Owner(db)

#     return render_template(
#         "activity_edit.html",
#         action=u"Nová",
#         owner=owner.get(request.args.get("owner"))
#     )


# @app.route("/activity_edit/", methods=["POST"])
# @login_required
# def activity_edit():
#     form = EditActivityForm(request.form)

#     if form.validate():
#         owner = Owner(db)

#         if not form.act_id.data:
#             flash(u"Nastala chyba při úpravě aktivity.", "error")
#             return redirect(url_for("owner_detail", owner_id=form.owner.data))

#         return render_template(
#             "activity_edit.html",
#             action="Upravit",
#             channelList=Activity(db).get_channels(),
#             channel=form.channel.data,
#             date=form.date.data,
#             result=form.result.data,
#             note=("" if form.note.data == "None" else form.note.data),
#             owner=owner.get(form.owner.data),
#             act_id=form.act_id.data
#         )

#     else:
#         flash(u"Nastala chyba při úpravě aktivity.", "error")
#         return redirect(url_for("activities"))


# @app.route("/calendar/")
# @login_required
# def calendar():
#     return render_template("calendar.html")






# ##############
# # user methods




# @app.route("/user_create/", methods=["GET", "POST"])
# @login_required
# def user_create():
#     form = CreateUserForm(request.form)

#     if request.method == "POST" and form.validate():
#         # passwords must match
#         if form.password.data != form.password_check.data:
#             flash(u"Hesla se neshodují", "error")
#             return redirect(url_for("user_create"))

#         User(form.login.data, db).create(
#            form.mail.data,
#            form.name.data,
#            form.password.data
#         )

#         return redirect(url_for("login"))

#     else:
#         return render_template("user_create.html")


# ####################
# # downloader methods

# @app.route("/append_to_download_queue/", methods=["POST"])
# @login_required
# def append_to_download_queue():
#     form = LrManipulateForm(request.form)
#     if form.validate():
#         downloader.add_to_queue(form.lr_number.data)

#     return redirect(url_for("downloads"))


# @app.route("/delete_from_download_queue/", methods=["POST"])
# @login_required
# def delete_from_download_queue():
#     form = LrManipulateForm(request.form)
#     if form.validate():
#         downloader.delete_from_download_queue(form.lr_number.data)

#     return redirect(url_for("downloads"))


# @app.route("/prior_download/", methods=["POST"])
# @login_required
# def prior_download():
#     form = LrManipulateForm(request.form)
#     if form.validate():
#         downloader.prior_download(form.lr_number.data)

#     return redirect(url_for("downloads"))


# @app.route("/start_download/", methods=["POST"])
# @login_required
# def start_download():
#     downloader.start()

#     return redirect(url_for("downloads"))


# @app.route("/stop_download/", methods=["POST"])
# @login_required
# def stop_download():
#     downloader.stop()

#     return redirect(url_for("downloads"))


# @app.route("/delete_from_download_bar/", methods=["POST"])
# @login_required
# def delete_from_download_bar():
#     downloader.delete_from_download_bar()

#     return redirect(url_for("downloads"))


# @app.route("/download_queue_up/", methods=["POST"])
# @login_required
# def download_queue_up():
#     form = LrManipulateForm(request.form)
#     if form.validate():
#         downloader.up_in_queue(form.lr_number.data)

#     return redirect(url_for("downloads"))


# @app.route("/download_queue_down/", methods=["POST"])
# @login_required
# def download_queue_down():
#     form = LrManipulateForm(request.form)
#     if form.validate():
#         downloader.down_in_queue(form.lr_number.data)

#     return redirect(url_for("downloads"))


# #################
# # scanner methods

# @app.route("/append_to_scan_queue/", methods=["POST"])
# @login_required
# def append_to_scan_queue():
#     form = ScannerAddForm(request.form)
#     if form.validate():
#         lr = LandRegister(db)
#         register = lr.get(form.lr_id.data)

#         # user must confirm deleting old data
#         if register and not form.force.data == "delete":
#             return render_template(
#                 "submit_lr_delete.html",
#                 lr_id=form.lr_id.data,
#                 lr_name=register["lr_name"]
#             )

#         # delete old data
#         if register:
#             res = lr.delete_lr_data(form.lr_id.data, downloader)

#             if not res:
#                 msg = u"nepodařilo se smazat existující katastr (stahuje se?)"


#         # validate and create new lr
#         else:
#             res = lr.create(form.lr_id.data, form.lr_name.data.encode('utf-8'))

#             if not res:
#                 msg = u"nepodařilo se vytvořt zadaný katastr"

#         if res:
#             scanner.add_to_queue(form.lr_id.data)
#             flash(u"Katastr úspěšně přidán.", "success")
#         else:
#             flash(u"Katastr se nepodařilo přidat - "+msg, "error")

#     return redirect(url_for("scans"))


# @app.route("/delete_from_scan_queue/", methods=["POST"])
# @login_required
# def delete_from_scan_queue():
#     form = LrManipulateForm(request.form)
#     if form.validate():
#         scanner.delete_from_scan_queue(form.lr_number.data)

#     return redirect(url_for("scans"))


# @app.route("/prior_scan/", methods=["POST"])
# @login_required
# def prior_scan():
#     form = LrManipulateForm(request.form)
#     if form.validate():
#         scanner.prior_scan(form.lr_number.data)

#     return redirect(url_for("scans"))


# @app.route("/start_scan/", methods=["POST"])
# @login_required
# def start_scan():
#     scanner.start()

#     return redirect(url_for("scans"))


# @app.route("/stop_scan/", methods=["POST"])
# @login_required
# def stop_scan():
#     scanner.stop()

#     return redirect(url_for("scans"))


# @app.route("/delete_from_scan_bar/", methods=["POST"])
# @login_required
# def delete_from_scan_bar():
#     scanner.delete_from_scan_bar()

#     return redirect(url_for("scans"))


# @app.route("/scan_queue_up/", methods=["POST"])
# @login_required
# def scan_queue_up():
#     form = LrManipulateForm(request.form)
#     if form.validate():
#         scanner.up_in_queue(form.lr_number.data)

#     return redirect(url_for("scans"))


# @app.route("/scan_queue_down/", methods=["POST"])
# @login_required
# def scan_queue_down():
#     form = LrManipulateForm(request.form)
#     if form.validate():
#         scanner.down_in_queue(form.lr_number.data)

#     return redirect(url_for("scans"))


# ##################
# # activity methods

# @app.route("/activity_save/", methods=["POST"])
# @login_required
# def activity_save():
#     form = EditActivityForm(request.form)

#     if form.validate():
#         act = Activity(db)

#         act.save(
#             owner=form.owner.data,
#             act_id=form.act_id.data,
#             channel=form.channel.data,
#             date=form.date.data,
#             result=None if form.result.data=="None" else form.result.data,
#             note=("" if form.note.data == "None" else form.note.data),
#         )

#         flash(u"Aktivita úspěšně uložena.", "success")
#         return redirect(url_for("owner_detail", owner_id=form.owner.data))

#     else:
#         flash(u"Nastala chyba při úpravě aktivity.", "error")
#         return redirect(url_for("activities"))


# @app.route("/activity_delete/", methods=["POST"])
# @login_required
# def activity_delete():
#     form = DeleteActivityForm(request.form)

#     if form.validate():
#         act = Activity(db)
#         act.delete(form.act_id.data)
#         flash(u"Aktivita úspěšně smazána.", "success")
#         return redirect(url_for("owner_detail", owner_id=form.owner.data))

#     else:
#         flash(u"Nastala chyba při mazání aktivity.", "error")
#         return redirect(url_for("activities"))



# ###############
# # owner methods

# @app.route("/owner_note_save/", methods=["POST"])
# @login_required
# def owner_note_save():
#     form = OwnerNoteForm(request.form)

#     if form.validate():
#         owner = Owner(db)

#         owner.save_note(
#             owner_id=form.owner.data,
#             note=form.note.data
#         )

#         flash(u"Poznámka úspěšně uložena.", "success")
#         return redirect(url_for("owner_detail", owner_id=form.owner.data))

#     else:
#         flash(u"Nastala chyba při úpravě poznámky.", "error")
#         return redirect(url_for("owners"))


# @app.route("/owner_tags_set/", methods=["POST"])
# @login_required
# def owner_tags_set():
#     form = OwnerTagForm(request.form)

#     if form.validate():
#         owner = Owner(db)

#         try:
#             owner.set_tag(form.owner.data, form.data)

#         except ValueError:
#             flash(u"Při ukládání tagů došlo k chybě", "error")
#             return redirect(url_for("owners"))

#         flash(u"Tagy úspěšně uloženy.", "success")
#         return redirect(url_for("owner_detail", owner_id=form.owner.data))

#     else:
#         flash(u"Při ukládání tagů došlo k chybě", "error")
#         return redirect(url_for("owners"))



# @app.route("/owner_edit_save/", methods=["POST"])
# @login_required
# def owner_edit_save():
#     form = OwnerEditForm(request.form)

#     if form.validate():
#         owner = Owner(db)
#         res = owner.update({
#             "owner_id": form.owner_id.data,
#             "mail": form.mail.data,
#             "phone": form.phone.data,
#             "city": form.city.data,
#             "street": form.street.data,
#             "str_number": form.str_number.data,
#             "post_code": form.post_code.data,
#             "birth": form.birth.data
#         })

#         if res:
#             flash(u"Vlastník úspěšně upraven.", "info")
#             return redirect(url_for(
#                 "owner_detail",
#                 owner_id=int(form.owner_id.data)
#             ))

#     flash(u"Nastala chyba při úpravě vlastníka.", "error")
#     return redirect(url_for("owners"))

# @app.route("/reload/")
# @login_required
# def reload():
#     params = _default_params(request.args)
#     params["filters"] = {
#         "name": request.args.get("name"),
#         "lv_number": request.args.get("lv_number"),
#         "expanse": request.args.get("expanse", "all"),
#         "active": request.args.get("active", "all"),
#         "land_register": request.args.get("land_register"),
#         "city": request.args.get("city"),
#         "tag": request.args.get("tag")
#     }

#     lr = params["filters"]["land_register"]
#     if lr:
#         lr_number = LandRegister(db).get_number(params["filters"]["land_register"])

#         if lr_number is None:
#             flash(u"Nepodařilo se určit katastr.", "warning")

#         params["filters"]["lr_number"] = lr_number

#     owner = Owner(db)
#     data = owner.reload(**params)

#     pagination = Pagination(
#         params["page"],
#         params["per_page"],
#         owner.count(params["filters"])
#     )

#     # ugly hack - "land_register" cannot be legal filter for owner, so it is deleted
#     #               while processing filters, but needs to be present again for web
#     params["filters"]["land_register"] = lr

#     return render_template(
#         "reload.html",
#         pagination=pagination,
#         data=data,
#         **params
#     )

# @app.route("/funPage/", methods=["GET", "POST"])
# def funPage():
#     params = _default_params(request.args)
#     params["filters"] = {
#         "id": request.args.get("id"),
#     }
#     id = params["filters"]["id"]
#     if id is None or id=="":
#         id=0
#     link = VideoAdd(db).get(id)
#     link = link.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/")
#     link = link.replace("https://youtu.be/", "https://www.youtube.com/embed/")
#     return render_template("funpage.html", link=link, id=id)

# @app.route("/add_video/", methods=["GET", "POST"])
# @login_required
# def add_video():
#     form = AddVideo(request.form)

#     if request.method == "POST" and form.validate():


#         VideoAdd(db).create(
#            form.link.data,
#            form.name.data
#         )

#         return redirect(url_for("funPage"))

#     else:
#         return render_template("add_video.html")
