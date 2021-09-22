# flake8: noqa F401
from .auth import auth_blueprint

from .mail_message import message_blueprint

# from .admin import CortexAdminIndexView
from .admin import CortexAdminIndexView, DoctorAdminModelView
