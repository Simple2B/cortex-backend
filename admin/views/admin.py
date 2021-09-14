from flask import redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app.models import Doctor


class CortexAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        doctor: Doctor = current_user
        if not (doctor.is_authenticated and doctor.role == Doctor.UserRole.ADMIN):
            return redirect(url_for("main.index"))
        return super(CortexAdminIndexView, self).index()


class PanelView(ModelView):
    def is_accessible(self):
        doctor: Doctor = current_user
        return doctor.is_authenticated and doctor.role == Doctor.DoctorRole.ADMIN


# class UserAdminModelView(PanelView):
#     column_exclude_list = ["photos", "evaluations", "photo_contests"]
#     form_excluded_columns = ["photos", "evaluations", "photo_contests", "created_at"]
#     column_searchable_list = ["first_name", "last_name", "username"]
#     column_editable_list = ["role"]
#     can_create = False
#     can_edit = False
