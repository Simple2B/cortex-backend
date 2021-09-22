from flask import redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app.models import Doctor


class CortexAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        doctor: Doctor = current_user
        if not (doctor.is_authenticated and doctor.role == Doctor.DoctorRole.Admin):
            return redirect(url_for("auth.login"))
        return super(CortexAdminIndexView, self).index()


class PanelView(ModelView):
    def is_accessible(self):
        doctor: Doctor = current_user
        return doctor.is_authenticated and doctor.role == Doctor.DoctorRole.Admin


class DoctorAdminModelView(PanelView):
    form_excluded_columns = ["email_approved", "hash_password", "api_key"]
    column_exclude_list = ["hash_password", "api_key"]

    column_searchable_list = ["first_name", "last_name", "email"]
    column_editable_list = ["role"]
    column_filters = ["email"]

    page_size = 15
