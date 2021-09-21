# from app import db

from admin.config import BaseConfig as conf
from app.models import Doctor


def add_doctor_to_db(
    first_name=conf.ADMIN_FIRST_NAME,
    last_name=conf.ADMIN_LAST_NAME,
    email=conf.ADMIN_EMAIL,
    role=Doctor.DoctorRole.ADMIN,
    passwd="admin123",
):
    doctor = Doctor(
        first_name=first_name,
        last_name=last_name,
        email=email,
        role=role,
    )
    doctor.password = passwd
    doctor.save()
    return doctor


# def create_db(add_test_data: bool = False):
#     db.create_all()
#     add_admin_to_db()
#     if add_test_data:
#         from tests.database import add_test_data

#         add_test_data()
