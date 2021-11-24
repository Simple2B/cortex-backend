import datetime
import random
from app.models import (
    Client,
    Doctor,
    ClientCondition,
    Condition,
    Disease,
    ClientDisease,
)
from admin.database import add_doctor_to_db
from app.database import db_session

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

CONDITIONS = [
    "Dizziness",
    "Headaches",
    "Ear infections",
    "Nausea",
    "Neck Pain",
    "Epilepsy",
    "Chronic sinus",
    "Migraines",
    "Anxiety",
    "Depression",
    "Throat issues",
    "Thyroid problems",
    "Asthma",
    "Ulcers",
    "Numbness in hands",
    "Disc problems",
    "Infertility",
    "Menstrual disorders",
    "High blood pressure",
    "Heart problems",
    "Digestive problems",
    "Kidney problems",
    "Bladder problems",
    "Numbness in legs",
    "Numbness in feet",
    "Low back pain",
    "Hip pain",
    "Shoulder pain",
    "Obesity",
    "Hormonal imbalance",
    "Liver disease",
    "Chronic fatigue",
    "Gastric reflux",
    "Lupus",
    "Fibromyalgia",
    "Chest pain",
    "Trouble concentrating",
    "Knee pain",
    "Nervousness",
    "Midback pain",
]

DISEASES = [
    "Concussion",
    "Stroke",
    "Cancer",
    "Diabetes",
    "Heart Disease",
    "Seizures",
    "Spinal bone fracture",
    "Scoliosis",
]


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
            phone=CLIENT_NUMBER_PHONE.format(i),
            email=CLIENT_EMAIL.format(i),
            referring="Trevor",
            medications="medications",
            covid_tested_positive=["no", "yes", "null"][random.randint(0, 2)],
            covid_vaccine=["no", "yes", "null"][random.randint(0, 2)],
            stressful_level=i,
            consent_minor_child=[True, False][random.randint(0, 1)],
            consent_diagnostic_procedures=[True, False][random.randint(0, 1)],
            # relationship_child="relationship child",
        )

        client.save(False)

    for condition_name in CONDITIONS:
        Condition(name=condition_name).save(False)

    for disease_name in DISEASES:
        Disease(name=disease_name).save(False)

    for client_id in range(1, CLIENT_NUMBER + 1):
        condition_ids = {random.randint(1, len(CONDITIONS)) for _ in range(3)}
        for condition_id in condition_ids:
            ClientCondition(client_id=client_id, condition_id=condition_id).save(False)

    for client_id in range(1, CLIENT_NUMBER + 1):
        disease_ids = {random.randint(1, len(DISEASES)) for _ in range(2)}
        for disease_id in disease_ids:
            ClientDisease(client_id=client_id, disease_id=disease_id).save(False)

    db_session.commit()
