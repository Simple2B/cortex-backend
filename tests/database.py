import openpyxl
from pathlib import Path
from admin.config import BaseConfig as conf
from app.models import Doctor, Client

from app.logger import log


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
    doctor.save(True)

    return doctor


def generate_test_data():
    doctor = Doctor.query.first()

    xlsx_file = Path("admin", "clients.xlsx")
    wb_obj = openpyxl.load_workbook(xlsx_file)

    log(log.INFO, "wb_obj [%s] ", wb_obj)

    # Read the active sheet:
    sheet = wb_obj.active

    log(log.INFO, "sheet [%s] ", sheet)

    if not doctor:
        doctor = add_doctor_to_db()

    for i in range(2, len(sheet["A"]) + 1):
        # str_address = sheet[f"G{i}"].value
        # num = None
        # address = []
        # for word in sheet["G2"].value.split():
        #     if word.isdigit():
        #         num = word
        #     else:
        #         address.append(word)

        # " ".join(address)
        client = Client(
            first_name=sheet[f"B{i}"].value,
            last_name=sheet[f"D{i}"].value,
            birthday=sheet[f"E{i}"].value,
            address=sheet[f"G{i}"].value,
            city=sheet[f"I{i}"].value,
            state=sheet[f"J{i}"].value,
            zip=sheet[f"K{i}"].value,
            phone=sheet[f"M{i}"].value,
            email=sheet[f"L{i}"].value,
            referring=sheet[f"N{i}"].value,
            medications=None,
            covid_tested_positive="null",
            covid_vaccine="null",
            stressful_level=1,
            consent_minor_child=None,
            consent_diagnostic_procedures=None,
        )

    client.save()


# CLIENT_NUMBER = 10
# CLIENT_FIRST_NAME = [
#     "Alex",
#     "Marta",
#     "Mark",
#     "Ben",
#     "Sasha",
#     "John",
#     "Max",
#     "Poll",
#     "Leon",
#     "Sara",
# ]

# CLIENT_LAST_NAME = [
#     "London",
#     "Washington",
#     "Tween",
#     "Connor",
#     "Lenone",
#     "Bush",
#     "Clinton",
#     "Kennedy",
#     "Pearsone",
#     "Franclin",
# ]

# CLIENT_EMAIL = "email_{}@email.com"

# CLIENT_NUMBER_PHONE = "12345{:06d}"

# BASE_DATE_BIRTHDAY = datetime.date(year=1973, month=10, day=12)

# CONDITIONS = [
#     "Dizziness",
#     "Headaches",
#     "Ear infections",
#     "Nausea",
#     "Neck Pain",
#     "Epilepsy",
#     "Chronic sinus",
#     "Migraines",
#     "Anxiety",
#     "Depression",
#     "Throat issues",
#     "Thyroid problems",
#     "Asthma",
#     "Ulcers",
#     "Numbness in hands",
#     "Disc problems",
#     "Infertility",
#     "Menstrual disorders",
#     "High blood pressure",
#     "Heart problems",
#     "Digestive problems",
#     "Kidney problems",
#     "Bladder problems",
#     "Numbness in legs",
#     "Numbness in feet",
#     "Low back pain",
#     "Hip pain",
#     "Shoulder pain",
#     "Obesity",
#     "Hormonal imbalance",
#     "Liver disease",
#     "Chronic fatigue",
#     "Gastric reflux",
#     "Lupus",
#     "Fibromyalgia",
#     "Chest pain",
#     "Trouble concentrating",
#     "Knee pain",
#     "Nervousness",
#     "Midback pain",
# ]

# DISEASES = [
#     "Concussion",
#     "Stroke",
#     "Cancer",
#     "Diabetes",
#     "Heart Disease",
#     "Seizures",
#     "Spinal bone fracture",
#     "Scoliosis",
# ]


# def generate_test_data():
#     doctor = Doctor.query.first()
#     if not doctor:
#         doctor = add_doctor_to_db()

#     for i in range(CLIENT_NUMBER):
#         client = Client(
#             first_name=CLIENT_FIRST_NAME[random.randint(0, len(CLIENT_FIRST_NAME) - 1)],
#             last_name=CLIENT_LAST_NAME[random.randint(0, len(CLIENT_LAST_NAME) - 1)],
#             birthday=BASE_DATE_BIRTHDAY + datetime.timedelta(days=1),
#             address="Street",
#             city="NY",
#             state="US",
#             zip=12345,
#             phone=CLIENT_NUMBER_PHONE.format(i),
#             email=CLIENT_EMAIL.format(i),
#             referring="Trevor",
#             medications="medications",
#             covid_tested_positive=["no", "yes", "null"][random.randint(0, 2)],
#             covid_vaccine=["no", "yes", "null"][random.randint(0, 2)],
#             stressful_level=i,
#             consent_minor_child=[True, False][random.randint(0, 1)],
#             consent_diagnostic_procedures=[True, False][random.randint(0, 1)],
#             # relationship_child="relationship child",
#         )

#         client.save(False)

#     for condition_name in CONDITIONS:
#         Condition(name=condition_name).save(False)

#     for disease_name in DISEASES:
#         Disease(name=disease_name).save(False)

#     for client_id in range(1, CLIENT_NUMBER + 1):
#         condition_ids = {random.randint(1, len(CONDITIONS)) for _ in range(3)}
#         for condition_id in condition_ids:
#             ClientCondition(client_id=client_id, condition_id=condition_id).save(False)

#     for client_id in range(1, CLIENT_NUMBER + 1):
#         disease_ids = {random.randint(1, len(DISEASES)) for _ in range(2)}
#         for disease_id in disease_ids:
#             ClientDisease(client_id=client_id, disease_id=disease_id).save(False)

#     db_session.commit()
