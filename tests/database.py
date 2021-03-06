import datetime
import random
import openpyxl
from pathlib import Path
from admin.config import BaseConfig as conf
from app.models import Doctor, Client

from app.logger import log


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
    doctor.save(True)

    return doctor


def generate_data():
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
        phone = (
            (
                str(sheet[f"M{i}"].value)
                .replace("(", "")
                .replace(")", "")
                .replace(" ", "")
                .replace("-", "")
            )
            if sheet[f"M{i}"].value
            else None
        )
        client = Client(
            first_name=sheet[f"B{i}"].value,
            last_name=sheet[f"D{i}"].value,
            birthday=sheet[f"E{i}"].value,
            address=sheet[f"G{i}"].value,
            city=sheet[f"I{i}"].value,
            state=sheet[f"J{i}"].value,
            zip=sheet[f"K{i}"].value,
            phone=phone,
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


def generate_test_data():
    doctor = Doctor.query.first()
    if not doctor:
        doctor = add_doctor_to_db()

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
            covid_tested_positive="null",
            covid_vaccine="null",
            stressful_level=i,
            consent_minor_child=[True, False][random.randint(0, 1)],
            consent_diagnostic_procedures=[True, False][random.randint(0, 1)],
            # relationship_child="relationship child",
        )

        client.save(True)
