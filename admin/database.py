# from app import db
import datetime
import random
from admin.config import BaseConfig as conf
from app.models import Doctor, Reception, Client

CLIENT_NUMBER = 11
CLIENT_FIRST_NAME = [
    "Alex",
    "Marta",
    "Mark",
    "Ben",
    "Sasha",
    "John",
    "Max",
    "Poll",
    "Leon",
    "Sara",
    "Alex",
]

CLIENT_LAST_NAME = [
    "London",
    "Washington",
    "Tween",
    "Connor",
    "Lenone",
    "Bush",
    "Clinton",
    "Kennedy",
    "Pearsone",
    "Franclin",
    "Brown",
]

CLIENT_EMAIL = [
    "email_1@email.com",
    "email_2@email.com",
    "email_3@email.com",
    "email_4@email.com",
    "email_5@email.com",
    "email_6@email.com",
    "email_7@email.com",
    "email_8@email.com",
    "email_9@email.com",
    "email_10@email.com",
    "client@gmail.com",
]

CLIENT_NUMBER_PHONE = [
    "+18143519421",
    "+16143519421",
    "+14143519421",
    "+18643519421",
    "+14443519421",
    "+16143519444",
    "+16143555444",
    "+18188555444",
    "+14143519666",
    "+14143444666",
    "19077653340",
]

BASE_DATE_BIRTHDAY = datetime.date(year=1973, month=10, day=12)


def add_doctor_to_db(
    first_name=conf.ADMIN_FIRST_NAME,
    last_name=conf.ADMIN_LAST_NAME,
    email=conf.ADMIN_EMAIL,
    role=Doctor.DoctorRole.Admin,
    passwd=conf.ADMIN_PASSWORD,
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


def generate_test_data():
    doctor = Doctor.query.first()
    if not doctor:
        doctor = add_doctor_to_db()

    reception = Reception(
        date=datetime.datetime.now(),
        doctor_id=doctor.id,
    )

    reception.save()

    for i in range(CLIENT_NUMBER):
        client = Client(
            first_name=CLIENT_FIRST_NAME[i],
            last_name=CLIENT_LAST_NAME[i],
            birthday=BASE_DATE_BIRTHDAY + datetime.timedelta(days=1),
            address="Street",
            city="NY",
            state="US",
            zip=12345,
            phone=CLIENT_NUMBER_PHONE[i],
            email=CLIENT_EMAIL[i],
            referring="Trevor",
            medications="medications",
            covid_tested_positive=[False, True, None][random.randint(0, 2)],
            covid_vaccine=[False, True, None][random.randint(0, 2)],
            stressful_level=i,
            consent_minor_child=[True, False][random.randint(0, 1)],
            relationship_child="relationship child",
        )

        client.save()


# def create_db(add_test_data: bool = False):
#     db.create_all()
#     add_admin_to_db()
#     if add_test_data:
#         from tests.database import add_test_data

#         add_test_data()
