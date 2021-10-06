import datetime
import random
from app.models import Client, Doctor, QueueMember, Visit
from admin.database import add_doctor_to_db

CLIENT_NUMBER = 10
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
]

BASE_DATE_BIRTHDAY = datetime.date(year=1973, month=10, day=12)


def generate_test_data():
    doctor = Doctor.query.first()
    if not doctor:
        doctor = add_doctor_to_db()

    for i in range(CLIENT_NUMBER):
        client = Client(
            first_name=CLIENT_FIRST_NAME[random.randint(0, len(CLIENT_FIRST_NAME) - 1)],
            last_name=CLIENT_LAST_NAME[random.randint(0, len(CLIENT_LAST_NAME) - 1)],
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
