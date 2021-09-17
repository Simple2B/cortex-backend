from flask import redirect, url_for, session, abort, render_template, request
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app.models import Doctor


class CortexAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        # doctor: Doctor = current_user
        # if not (doctor.is_authenticated and doctor.role == Doctor.DoctorRole.ADMIN):
        #     return redirect("")
        return super(CortexAdminIndexView, self).index()


class PanelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            return abort(403)

        # doctor: Doctor = current_user
        # return doctor.is_authenticated and doctor.role == Doctor.DoctorRole.ADMIN

    # def inaccessible_callback(self):
    #     # redirect to login page if user doesn't have access
    #     return redirect(url_for("run.login", next=request.url))


class DoctorAdminModelView(PanelView):
    column_exclude_list = ["doctors", "clients"]
    form_excluded_columns = ["doctors", "clients"]
    column_searchable_list = ["first_name", "last_name", "email"]
    column_editable_list = ["role"]

    column_filters = ["email"]
    column_exclude_list = ["email"]
    # can_create = False
    # can_edit = False
    page_size = 15
