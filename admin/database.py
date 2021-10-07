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

CLIENT_EMAIL = "email_{}@email.com"

CLIENT_NUMBER_PHONE = "12345{:06d}"

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

    reception = Reception(
        date=datetime.datetime.now(),
        doctor_id=doctor.id,
    )

    reception.save()

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
            phone=CLIENT_NUMBER_PHONE.format(i),
            email=CLIENT_EMAIL.format(i),
            referring="Trevor",
            medications="medications",
            covid_tested_positive=[False, True, None][random.randint(0, 2)],
            covid_vaccine=[False, True, None][random.randint(0, 2)],
            stressful_level=i,
            consent_minor_child=[True, False][random.randint(0, 1)],
            relationship_child="relationship child",
        )

        client.save()
