import datetime

from fastapi import HTTPException, status
from app.schemas import (
    Doctor,
    PostTest,
    CreateTest,
    GetTest,
    PostTestCarePlanAndFrequency,
    CarePlanCreate,
)
from app.models import Client as ClientDB, Test, InfoCarePlan, InfoFrequency, CarePlan
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

        create_test: Test = Test(
            date=date,
            client_id=client.id,
            doctor_id=doctor.id,
        ).save()

        return create_test

    def write_care_plan_frequency(
        self, data: PostTestCarePlanAndFrequency, doctor: Doctor
    ) -> CreateTest:
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
        test: Test = Test.query.filter(Test.id == data.test_id).first()

        if not test:
            log(log.ERROR, "write_care_plan_frequency: Test not created")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="write_care_plan_frequency: Test not created",
            )

        log(log.INFO, "write_care_plan_frequency: Test [%d] found", test.id)

        test.care_plan = data.care_plan
        test.frequency = data.frequency
        test.save()

        info_care_plan = InfoCarePlan.query.filter(
            InfoCarePlan.care_plan == data.care_plan
        ).first()

        if not info_care_plan:
            care_plan = InfoCarePlan(
                care_plan=data.care_plan, doctor_id=doctor.id
            ).save()

            log(
                log.INFO,
                "write_care_plan_frequency: care_plan [%d] created",
                care_plan.id,
            )

        info_frequency = InfoFrequency.query.filter(
            InfoFrequency.frequency == data.frequency
        ).first()

        if not info_frequency:
            info_frequency = InfoFrequency(
                frequency=data.frequency, doctor_id=doctor.id
            ).save()
            log(
                log.INFO,
                "write_care_plan_frequency: info_frequency [%d] created",
                info_frequency.id,
            )

        return {
            "id": data.test_id,
            "client_id": client.id,
            "doctor_id": doctor.id,
            "care_plan": data.care_plan,
            "frequency": data.frequency,
        }

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
                    "care_plan": test.care_plan,
                    "frequency": test.frequency,
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

        return {
            "id": test.id,
            "date": test.date.strftime("%B %d %Y"),
            "client_name": test.client.first_name,
            "doctor_name": test.doctor.first_name,
            "care_plan": test.care_plan,
            "frequency": test.frequency,
        }
