# from app import db
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
            medications=[],
            covid_tested_positive="null",
            covid_vaccine="null",
            stressful_level=1,
            consent_minor_child=None,
            consent_diagnostic_procedures=None,
        )

        client.save()
