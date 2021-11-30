import datetime
import re

from fastapi import HTTPException, status
from app.schemas import (
    Doctor,
    PostTest,
    CreateTest,
    GetTest,
    PostTestCarePlanAndFrequency,
    CarePlanCreate,
)
from app.models import (
    Client as ClientDB,
    Test,
    InfoCarePlan,
    InfoFrequency,
    CarePlan,
)
from app.logger import log


class TestService:
    def care_plan_create(self, data: PostTest, doctor: Doctor) -> CarePlanCreate:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.api_key == data.api_key
        ).first()

        if not client:
            log(log.ERROR, "care_plan_create: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="care_plan_create: Client not found",
            )

        log(log.INFO, "care_plan_create: Client [%s] for test", client)

        care_plan: CarePlan = CarePlan.query.filter(
            CarePlan.client_id == client.id
        ).first()

        if not care_plan:
            care_plan = CarePlan(client_id=client.id, doctor_id=doctor.id).save()
            log(log.INFO, "care_plan_create: care plan [%d] created", care_plan.id)
            return care_plan
        log(log.INFO, "care_plan_create: care plan [%s]", care_plan)
        return care_plan

    def get_care_plan(self, api_key: str, doctor: Doctor) -> CarePlanCreate:
        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()

        if not client:
            log(log.ERROR, "get_care_plan: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="get_care_plan: Client not found",
            )

        log(log.INFO, "get_care_plan: Client [%s] for test", client)

        care_plan: CarePlan = CarePlan.query.filter(
            CarePlan.client_id == client.id
        ).first()

        if not care_plan:
            log(log.INFO, "get_care_plan: care plan not found")
            return
        return care_plan

    def create_test(self, data: PostTest, doctor: Doctor) -> CreateTest:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.api_key == data.api_key
        ).first()

        if not client:
            log(log.ERROR, "create_test: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="create_test: Client not found",
            )

        log(log.INFO, "create_test: Client [%s] for test", client)

        date = datetime.datetime.strptime(data.date, "%m/%d/%Y, %H:%M:%S")

        if not date:
            log(log.ERROR, "create_test: Date not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="create_test: Front end Data don't send",
            )

        log(log.INFO, "create_test: Date [%s] for start test", date)

        care_plan: CarePlan = CarePlan.query.filter(
            CarePlan.client_id == client.id
        ).first()

        if not care_plan:
            log(log.INFO, "create_test: care plan not created")
            return
        log(log.INFO, "create_test: care plan [%s]", care_plan)

        create_test: Test = Test(
            date=date,
            care_plan_id=care_plan.id,
            client_id=client.id,
            doctor_id=doctor.id,
        )
        create_test.save()

        return create_test

    def write_care_plan_frequency(
        self, data: PostTestCarePlanAndFrequency, doctor: Doctor
    ) -> CarePlanCreate:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.api_key == data.api_key
        ).first()

        if not client:
            log(log.ERROR, "write_care_plan_frequency: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="write_care_plan_frequency: Client not found",
            )

        log(log.INFO, "write_care_plan_frequency: Client [%s] for test", client)

        care_plan: CarePlan = CarePlan.query.filter(
            CarePlan.client_id == client.id
        ).first()
        # test: Test = Test.query.filter(Test.id == data.test_id).first()

        if not care_plan:
            log(log.ERROR, "write_care_plan_frequency: care plan not created")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="write_care_plan_frequency: care plan not created",
            )

        log(log.INFO, "write_care_plan_frequency: care plan [%d] found", care_plan.id)

        if data.care_plan == "" or data.frequency == "":
            log(
                log.INFO,
                "write_care_plan_frequency: care_plan [%s] or frequency [%s] not filled",
                data.care_plan,
                data.frequency,
            )
            return care_plan

        data_care_plan = ""

        month_data_care_plan = re.findall("m", data.care_plan)
        week_data_care_plan = re.findall("w", data.care_plan)

        if len(month_data_care_plan) > 0:
            num_care_plan = re.findall(r"\d+", data.care_plan)
            data_care_plan = num_care_plan[0] + "-" + "month"

        if len(week_data_care_plan) > 0:
            num_care_plan = re.findall(r"\d+", data.care_plan)
            data_care_plan = num_care_plan[0] + "-" + "week"

        log(log.INFO, "write_care_plan_frequency: data_care_plan [%s]", data_care_plan)

        data_frequency = ""

        month_data_frequency = re.findall("m", data.frequency)
        week_data_frequency = re.findall("w", data.frequency)

        if len(month_data_frequency) > 0:
            num_frequency = re.findall(r"\d+", data.frequency)
            data_frequency = num_frequency[0] + "-" + "month"

        if len(week_data_frequency) > 0:
            num_frequency = re.findall(r"\d+", data.frequency)
            data_frequency = num_frequency[0] + "-" + "week"

        log(log.INFO, "write_care_plan_frequency: data_frequency [%s]", data_frequency)

        if data_care_plan == "" or data_frequency == "":
            log(
                log.INFO,
                "write_care_plan_frequency: data_care_plan [%s] or data_frequency [%s] not filled",
                data.care_plan,
                data.frequency,
            )
            return care_plan

        care_plan.care_plan = data_care_plan
        care_plan.frequency = data_frequency
        care_plan.client_id = client.id
        care_plan.doctor_id = doctor.id
        care_plan.save()

        log(
            log.INFO,
            "write_care_plan_frequency: care plan [%d] with care_plan [%s] and frequency[%s] saved",
            care_plan.id,
            care_plan.care_plan,
            care_plan.frequency,
        )

        info_care_plan = InfoCarePlan.query.filter(
            InfoCarePlan.care_plan == data_care_plan
        ).first()

        if not info_care_plan:
            info_care_plan = InfoCarePlan(
                care_plan=data_care_plan, doctor_id=doctor.id
            ).save()

            log(
                log.INFO,
                "write_care_plan_frequency: info_care_plan [%d] created",
                info_care_plan.id,
            )

        info_frequency = InfoFrequency.query.filter(
            InfoFrequency.frequency == data_frequency
        ).first()

        if not info_frequency:
            info_frequency = InfoFrequency(
                frequency=data_frequency, doctor_id=doctor.id
            ).save()
            log(
                log.INFO,
                "write_care_plan_frequency: info_frequency [%d] created",
                info_frequency.id,
            )
        return care_plan

    def get_client_tests(self, api_key: str, doctor: Doctor) -> list[GetTest]:
        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()

        if not client:
            log(log.ERROR, "get_client_tests: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="get_client_tests: Client not found",
            )

        log(log.INFO, "get_client_tests: Client [%s] for test", client)

        tests: Test = Test.query.filter(Test.client_id == client.id).all()

        all_tests = []

        for test in tests:
            all_tests.append(
                {
                    "id": test.id,
                    "date": test.date.strftime("%B %d %Y"),
                    "care_plan_id": test.care_plan_id,
                    "client_name": client.first_name,
                    "doctor_name": doctor.first_name,
                }
            )

        log(log.INFO, "get_client_tests: Count of tests [%d]", len(all_tests))

        return all_tests

    def get_care_plan_names(self, doctor: Doctor) -> InfoCarePlan:
        care_plan_names = InfoCarePlan.query.all()
        if not care_plan_names:
            log(log.INFO, "get_care_plan_names: No care plan names")
            return
        log(log.INFO, "get_care_plan_names: Count of names [%d]", len(care_plan_names))
        return care_plan_names

    def get_frequency_names(self, doctor: Doctor) -> InfoFrequency:
        frequency_plan_names = InfoFrequency.query.all()
        if not frequency_plan_names:
            log(log.INFO, "get_frequency_names: No care plan names")
            return
        log(
            log.INFO,
            "get_frequency_names: Count of frequency names [%d]",
            len(frequency_plan_names),
        )
        return frequency_plan_names

    def get_test(self, test_id: str, doctor: Doctor) -> GetTest:
        id = int(test_id)
        if not id:
            log(log.INFO, "get_test: No test id")
            return
        test: Test = Test.query.filter(Test.id == id).first()
        if not test:
            log(log.INFO, "get_test: No test")
            return
        log(log.INFO, "get_test: Test [%d]", test.id)

        care_plan: CarePlan = CarePlan.query.filter(
            CarePlan.id == test.care_plan_id
        ).first()

        if not care_plan:
            log(log.INFO, "get_test: care plan doesn't created")

        log(log.INFO, "get_test: care plan [%d] for test [%d]", care_plan.id, test.id)

        return {
            "id": test.id,
            "date": test.date.strftime("%B %d %Y"),
            "client_name": test.client.first_name,
            "doctor_name": test.doctor.first_name,
            "care_plan_id": test.care_plan_id,
            "care_plan": care_plan.care_plan,
            "frequency": care_plan.frequency,
        }
