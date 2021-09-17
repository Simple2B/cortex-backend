from flask import redirect, url_for
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app.models import Doctor


class CortexAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        doctor: Doctor = current_user
        # if not (doctor.is_authenticated and doctor.role == Doctor.DoctorRole.ADMIN):
        #     return redirect("https://cortex.simple2b.net/login")
        return super(CortexAdminIndexView, self).index()


class PanelView(ModelView):
    def is_accessible(self):
        doctor: Doctor = current_user
        return doctor.is_authenticated and doctor.role == Doctor.DoctorRole.ADMIN


class DoctorAdminModelView(PanelView):
    column_exclude_list = ["doctors", "clients", "visits"]
    form_excluded_columns = ["doctors", "clients", "visits", "created_at"]
    column_searchable_list = ["first_name", "last_name", "email"]
    column_editable_list = ["role"]
    can_create = False
    can_edit = False
