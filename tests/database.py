import datetime
import random
from app.models import Client, Doctor, Visit, Reception, QueueMember
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

CLIENT_EMAIL = "email_{}@email.com"

CLIENT_NUMBER_PHONE = "12345{:06d}"

BASE_DATE_BIRTHDAY = datetime.date(year=1973, month=10, day=12)


def generate_test_data():
    doctor = Doctor.query.first()
    if not doctor:
        doctor = add_doctor_to_db()

    reception = Reception.query.filter(Reception.doctor_id == doctor.id).first()
    reception.date = datetime.datetime.now()
    reception.save()

    for i in range(CLIENT_NUMBER):
        client = Client(
            first_name=CLIENT_FIRST_NAME[random.randint(0, len(CLIENT_FIRST_NAME) - 1)],
            last_name=CLIENT_LAST_NAME[random.randint(0, len(CLIENT_LAST_NAME) - 1)],
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

        visit = Visit(
            data_time=datetime.datetime.now(),
            # TODO duration => may be end of visit
            rougue_mode=[True, False][random.randint(0, 1)],
            client_id=client.id,
            doctor_id=doctor.id,
        )
        visit.save()

        queue_member = QueueMember(
            place_in_queue=i,
            canceled=[True, False][random.randint(0, 1)],
            client_id=client.id,
            visit_id=visit.id,
            reception_id=reception.id,
        )

        queue_member.save()
