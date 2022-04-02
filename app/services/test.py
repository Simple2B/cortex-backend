import re
import datetime
from typing import Union

from fastapi import HTTPException, status
from app.schemas import (
    Doctor,
    PostTest,
    CreateTest,
    GetTest,
    ClientCarePlan,
    PostTestCarePlanAndFrequency,
    CarePlanCreate,
    CarePlanPatientInfo,
    InfoCarePlan as typeInfoCarePlan,
    InfoFrequency as typeInfoFrequency,
    CarePlanHistory,
    CurrentCarePlan,
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
    def care_plan_create(self, data: ClientCarePlan, doctor: Doctor) -> CurrentCarePlan:
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

        care_plans: CarePlan = CarePlan.query.filter(
            CarePlan.client_id == client.id
        ).all()

        if len(care_plans) == 0:
            return self.new_care_plan_data(client, doctor)

        today = datetime.datetime.utcnow()
        history_care_plans = []
        for care_plan in care_plans:
            if datetime.datetime.strptime(
                care_plan.start_time.strftime("%m/%d/%Y"), "%m/%d/%Y"
            ) == datetime.datetime.strptime(today.strftime("%m/%d/%Y"), "%m/%d/%Y"):
                return {
                    "id": care_plan.id,
                    "date": care_plan.date.strftime("%m/%d/%Y"),
                    "start_time": care_plan.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
                    "end_time": care_plan.end_time.strftime("%m/%d/%Y, %H:%M:%S")
                    if care_plan.end_time
                    else None,
                    "care_plan": care_plan.care_plan,
                    "frequency": care_plan.frequency,
                    "progress_date": care_plan.progress_date.strftime(
                        "%m/%d/%Y, %H:%M:%S"
                    )
                    if care_plan.progress_date
                    else None,
                    "client_id": care_plan.client_id,
                    "doctor_id": care_plan.doctor_id,
                }
            if care_plan.end_time is None or care_plan.end_time >= today:
                if data.start_time or data.start_time:
                    self.update_care_plan(care_plan, data.start_time, data.end_time)
            if care_plan.end_time and care_plan.end_time < today:
                history_care_plans.append(care_plan)
        if len(care_plans) == len(history_care_plans):
            return self.new_care_plan_data(client, doctor)

    def get_care_plan(
        self, api_key: str, doctor: Doctor
    ) -> Union[typeInfoCarePlan, None]:
        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()

        if not client:
            log(log.ERROR, "get_care_plan: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="get_care_plan: Client not found",
            )

        log(log.INFO, "get_care_plan: Client [%s] for test", client)

        care_plans: CarePlan = CarePlan.query.filter(
            CarePlan.client_id == client.id
        ).all()

        if len(care_plans) == 0:
            log(log.INFO, "get_care_plan: care plan not found")
            return

        today = datetime.datetime.now()
        care_plan = None
        for plan in care_plans:
            if plan.start_time and plan.end_time is None:
                care_plan = self.get_data_care_plan(plan, client, doctor)

            if plan.start_time < today and (plan.end_time and plan.end_time >= today):
                care_plan = self.get_data_care_plan(plan, client, doctor)
        return care_plan

    def get_history_care_plan(
        self, api_key: str, doctor: Doctor
    ) -> CarePlanHistory or None:
        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()
        if not client:
            log(log.ERROR, "get_history_care_plan: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "get_history_care_plan: Client [%s]", client)
        care_plans: CarePlan = CarePlan.query.filter(
            CarePlan.client_id == client.id
        ).all()
        log(log.INFO, "get_history_care_plan: care_plans length [%d]", len(care_plans))

        history_care_plans = []
        for care_plan in care_plans:
            if care_plan.end_time:
                history_care_plans.append(care_plan)
        log(
            log.INFO,
            "get_history_care_plan: history_care_plans length[%d]",
            len(history_care_plans),
        )
        if len(history_care_plans) > 0:
            care_plans = []
            for care_plan in history_care_plans:
                history_care_plans
                visits = care_plan.care_plan_info_tests["visits"]
                notes = None
                if len(visits) > 0:
                    for visit in visits:
                        if (
                            visit.start_time >= care_plan.start_time
                            and visit.end_time is None
                            or visit.start_time >= care_plan.start_time
                            and visit.end_time <= care_plan.end_time
                        ):
                            notes = [
                                {
                                    "id": note.id,
                                    "date": note.date,
                                    "client_id": note.client_id,
                                    "doctor_id": note.doctor_id,
                                    "note": note.notes,
                                }
                                for note in visit.visit_info["notes"]
                            ]

                care_plans.append(
                    {
                        "id": care_plan.id,
                        "date": care_plan.date.strftime("%m/%d/%Y"),
                        "start_time": care_plan.start_time.strftime(
                            "%m/%d/%Y, %H:%M:%S"
                        ),
                        "end_time": care_plan.end_time.strftime("%m/%d/%Y, %H:%M:%S"),
                        "care_plan": care_plan.care_plan,
                        "frequency": care_plan.frequency,
                        "progress_date": care_plan.progress_date.strftime(
                            "%m/%d/%Y, %H:%M:%S"
                        )
                        if care_plan.progress_date
                        else care_plan.progress_date,
                        "client_id": care_plan.client_id,
                        "doctor_id": care_plan.doctor_id,
                        "doctor_name": doctor.first_name + " " + doctor.last_name,
                        "tests": care_plan.care_plan_info_tests["tests"],
                        "notes": notes if notes else [],
                    }
                )
            return care_plans
        return []

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

        care_plan = CarePlan.query.filter(
            CarePlan.id == data.current_care_plan_id
        ).first()

        if not care_plan:
            log(log.ERROR, "create_test: Care plan not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="create_test: Care plan not found",
            )

        log(log.INFO, "create_test: care plan [%s]", care_plan)

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
            care_plan_id=care_plan.id,
            client_id=client.id,
            doctor_id=doctor.id,
        )
        create_test.save()

        return create_test

    @staticmethod
    def update_care_plan(care_plan, start_time, end_time):
        if start_time:
            care_plan.start_time = datetime.datetime.strptime(
                start_time, "%m/%d/%Y, %H:%M:%S"
            )
            care_plan.save(True)
        if end_time:
            care_plan.end_time = datetime.datetime.strptime(
                end_time, "%m/%d/%Y, %H:%M:%S"
            )
            care_plan.save(True)
        log(log.INFO, "update_care_plan: care plan [%s] updated", care_plan)
        return {
            "id": care_plan.id,
            "date": care_plan.date.strftime("%m/%d/%Y, %H:%M:%S"),
            "start_time": care_plan.start_time.strftime("%m/%d/%Y, %H:%M:%S")
            if care_plan.start_time
            else None,
            "end_time": care_plan.end_time.strftime("%m/%d/%Y, %H:%M:%S")
            if care_plan.end_time
            else None,
            "care_plan": care_plan.care_plan,
            "frequency": care_plan.frequency,
            "progress_date": care_plan.progress_date.strftime("%m/%d/%Y, %H:%M:%S")
            if care_plan.progress_date
            else care_plan.progress_date,
            "client_id": care_plan.client_id,
            "doctor_id": care_plan.doctor_id,
        }

    @staticmethod
    def new_care_plan_data(client: ClientDB, doctor: Doctor) -> CurrentCarePlan:
        care_plan = CarePlan(
            client_id=client.id,
            doctor_id=doctor.id,
        ).save()
        log(log.INFO, "new_care_plan_data: care plan [%s] created", care_plan)
        return {
            "id": care_plan.id,
            "date": care_plan.date.strftime("%m/%d/%Y, %H:%M:%S"),
            "start_time": care_plan.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            "end_time": care_plan.end_time,
            "care_plan": care_plan.care_plan,
            "frequency": care_plan.frequency,
            "progress_date": care_plan.progress_date,
            "client_id": care_plan.client_id,
            "doctor_id": care_plan.doctor_id,
        }

    @staticmethod
    def get_data_care_plan(plan, client: ClientDB, doctor: Doctor) -> typeInfoCarePlan:
        return {
            "date": plan.date if plan.date else None,
            "start_time": plan.start_time.strftime("%m/%d/%Y, %H:%M:%S")
            if plan.start_time
            else None,
            "end_time": plan.end_time.strftime("%m/%d/%Y, %H:%M:%S")
            if plan.end_time
            else None,
            "progress_date": plan.progress_date.strftime("%m/%d/%Y, %H:%M:%S")
            if plan.progress_date
            else None,
            "care_plan": plan.care_plan,
            "frequency": plan.frequency,
            "client_id": client.id,
            "doctor_id": doctor.id,
        }

    @staticmethod
    def formed_care_plan_with_progress_test_date(
        care_plan,
        data_care_plan: str,
        data_frequency: str,
        progress_date,
        client,
        doctor,
    ) -> CarePlanCreate:
        care_plan.care_plan = data_care_plan
        care_plan.frequency = data_frequency
        care_plan.progress_date = progress_date
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

        res_care_plan = {
            "date": care_plan.date,
            "progress_date": care_plan.progress_date.strftime("%m/%d/%Y, %H:%M:%S"),
            "care_plan": care_plan.care_plan,
            "frequency": care_plan.frequency,
            "client_id": care_plan.client_id,
            "doctor_id": care_plan.doctor_id,
        }
        return res_care_plan

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

        care_plans: CarePlan = CarePlan.query.filter(
            CarePlan.client_id == client.id
        ).all()

        if len(care_plans) == 0:
            log(log.ERROR, "write_care_plan_frequency: care plan not created")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="write_care_plan_frequency: care plan not created",
            )

        log(
            log.INFO,
            "write_care_plan_frequency: count of care plans [%d]",
            len(care_plans),
        )
        today = datetime.datetime.utcnow()

        for care_plan in care_plans:
            if (
                care_plan.end_time is None
                or care_plan.end_time
                and care_plan.end_time >= today
            ):

                data_care_plan = ""

                if len(data.care_plan) > 0:
                    month_data_care_plan = re.findall("m", data.care_plan)
                    week_data_care_plan = re.findall("w", data.care_plan)

                    if len(month_data_care_plan) > 0:
                        num_care_plan = re.findall(r"\d+", data.care_plan)
                        data_care_plan = num_care_plan[0] + "-" + "month"

                    if len(week_data_care_plan) > 0:
                        num_care_plan = re.findall(r"\d+", data.care_plan)
                        data_care_plan = num_care_plan[0] + "-" + "week"

                    log(
                        log.INFO,
                        "write_care_plan_frequency: data_care_plan [%s]",
                        data_care_plan,
                    )

                data_frequency = ""

                if len(data.frequency) > 0:
                    month_data_frequency = re.findall("m", data.frequency)
                    week_data_frequency = re.findall("w", data.frequency)

                    if len(month_data_frequency) > 0:
                        num_frequency = re.findall(r"\d+", data.frequency)
                        data_frequency = num_frequency[0] + "-" + "month"

                    if len(week_data_frequency) > 0:
                        num_frequency = re.findall(r"\d+", data.frequency)
                        data_frequency = num_frequency[0] + "-" + "week"

                    log(
                        log.INFO,
                        "write_care_plan_frequency: data_frequency [%s]",
                        data_frequency,
                    )

                progress_date = None
                # if the progress_date is not filled,
                # the next test date should occur 6 weeks(42 days) after the patient's last test
                if not data.progress_date:
                    tests = care_plan.care_plan_info_tests["tests"]
                    if len(tests) > 0:
                        last_test = tests[-1]
                        progress_date = last_test.date + datetime.timedelta(days=42)
                        log(
                            log.INFO,
                            "write_care_plan_frequency: progress_date [%s] from last test",
                            progress_date,
                        )

                        care_plan = self.formed_care_plan_with_progress_test_date(
                            care_plan,
                            data_care_plan,
                            data_frequency,
                            progress_date,
                            client,
                            doctor,
                        )
                        return care_plan

                progress_date = datetime.datetime.strptime(
                    data.progress_date, "%m/%d/%Y, %H:%M:%S"
                )

                log(
                    log.INFO,
                    "write_care_plan_frequency: progress_date [%s] from doctor",
                    progress_date,
                )

                care_plan = self.formed_care_plan_with_progress_test_date(
                    care_plan,
                    data_care_plan,
                    data_frequency,
                    progress_date,
                    client,
                    doctor,
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

        care_plans: CarePlan = CarePlan.query.filter(
            CarePlan.client_id == client.id
        ).all()

        if len(care_plans) == 0:
            log(log.INFO, "get_client_tests: care plan didn't create yet")
            return []

        today = datetime.datetime.utcnow()

        for care_plan in care_plans:
            if care_plan.end_time is None:
                all_tests = self.get_tests_info(care_plan, client, doctor)
                return all_tests
            if care_plan.end_time and care_plan.end_time >= today:
                all_tests = self.get_tests_info(care_plan, client, doctor)
                return all_tests

        return []

    def get_care_plan_names(self, doctor: Doctor) -> typeInfoCarePlan:
        care_plan_names = InfoCarePlan.query.all()
        if not care_plan_names:
            log(log.INFO, "get_care_plan_names: No care plan names")
            return [{"number": 0, "care_plan": ""}]
        log(log.INFO, "get_care_plan_names: Count of names [%d]", len(care_plan_names))
        names = []
        for name in care_plan_names:
            num_name = re.findall(r"\d+", name.care_plan)
            log(log.INFO, "get_care_plan_names: num_name [%s]", num_name)
            if len(num_name) > 0:
                log(log.INFO, "get_care_plan_names: [%d]", len(num_name))
                names.append({"number": int(num_name[0]), "care_plan": name.care_plan})

        sorted_names = sorted(names, key=lambda k: k["number"])
        log(log.INFO, "get_care_plan_names: names are sorted")

        return sorted_names

    def get_frequency_names(self, doctor: Doctor) -> typeInfoFrequency:
        frequency_plan_names = InfoFrequency.query.all()
        if not frequency_plan_names:
            log(log.INFO, "get_frequency_names: No care plan names")
            return [{"number": 0, "frequency": ""}]
        log(
            log.INFO,
            "get_frequency_names: Count of frequency names [%d]",
            len(frequency_plan_names),
        )
        names = []
        for name in frequency_plan_names:
            num_name = re.findall(r"\d+", name.frequency)
            log(log.INFO, "get_frequency_names: num_name [%s]", num_name)
            if len(num_name) > 0:
                log(log.INFO, "get_frequency_names: [%d]", len(num_name))
                names.append({"number": int(num_name[0]), "frequency": name.frequency})

        sorted_names = sorted(names, key=lambda k: k["number"])
        log(log.INFO, "get_frequency_names: names are sorted")

        return sorted_names

    def get_test(self, test_id: str, doctor: Doctor) -> GetTest:
        id = int(test_id)
        if not id:
            log(log.INFO, "get_test: No id")
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

    def get_info_for_care_plan_page(
        self, api_key: str, doctor: Doctor
    ) -> CarePlanPatientInfo:
        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()

        if not client:
            log(log.ERROR, "get_info_for_care_plan_page: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="get_info_for_care_plan_page: Client not found",
            )

        log(log.INFO, "get_info_for_care_plan_page: Client [%s] for test", client)

        visits = client.client_info["visits"]
        if len(visits):
            first_visit = visits[0]
            last_visit = visits[-1]

        care_plans: CarePlan = CarePlan.query.filter(
            CarePlan.client_id == client.id
        ).all()
        care_plan = care_plans[-1]

        care_plan_length = None
        visit_frequency = None
        next_visit = None
        care_plan_length = None
        visit_frequency = None
        next_visit = None
        if not care_plan:
            return {
                "first_visit": "-",
                "last_visit": "-",
                "total_visits": "-",
                "care_plan_length": "-",
                "visit_frequency": "-",
                "next_visit": "-",
                "expiration": "-",
            }

        care_plan_length = care_plan.care_plan
        if not care_plan_length:
            care_plan_length = "-"

        visit_frequency = care_plan.frequency
        if not visit_frequency:
            visit_frequency = "-"

        # "%m/%d/%Y, %H:%M:%S"
        if care_plan.progress_date:
            next_visit = care_plan.progress_date.strftime("%m/%d/%Y")
        else:
            next_visit = "-"

        return {
            "first_visit": first_visit.start_time.strftime("%m/%d/%Y"),
            "last_visit": last_visit.start_time.strftime("%m/%d/%Y"),
            "total_visits": len(visits),
            "care_plan_length": care_plan_length,
            "visit_frequency": visit_frequency,
            "next_visit": next_visit,
            "expiration": "",
        }

    @staticmethod
    def get_tests_info(
        care_plan: CarePlan, client: ClientDB, doctor: Doctor
    ) -> list[GetTest]:
        tests: Test = Test.query.filter(Test.care_plan_id == care_plan.id).all()
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
