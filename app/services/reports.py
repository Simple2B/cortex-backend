import datetime
from typing import List
import csv

from app.schemas import (
    Doctor,
    VisitReportReq,
    VisitReportRes,
)
from app.models import Visit

from app.logger import log


class ReportService:
    @staticmethod
    def get_visits_for_report(all_visits: list, start_time: str, end_time: str) -> list:
        visits_report = []
        for visit in all_visits:
            if visit.end_time:
                visit_start_time = datetime.datetime.strptime(
                    visit.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
                    "%m/%d/%Y, %H:%M:%S",
                )
                visit_end_time = datetime.datetime.strptime(
                    visit.end_time.strftime("%m/%d/%Y, %H:%M:%S"),
                    "%m/%d/%Y, %H:%M:%S",
                )
                if visit_start_time >= datetime.datetime.strptime(
                    start_time, "%m/%d/%Y, %H:%M:%S"
                ) and visit_end_time <= datetime.datetime.strptime(
                    end_time, "%m/%d/%Y, %H:%M:%S"
                ):
                    visits_report.append(visit)
        return visits_report

    def filter_data_for_report_of_visit(
        self, client_data: VisitReportReq, doctor: Doctor
    ) -> List[VisitReportRes]:
        log(
            log.INFO,
            "filter_data_for_report_of_visit: client_data [%s]",
            client_data,
        )
        start_time = client_data.start_time
        end_time = client_data.end_time

        log(
            log.INFO,
            "filter_data_for_report_of_visit: start_time [%s] and end_time [%s] from client_data",
            start_time,
            end_time,
        )

        if client_data.type == "visits":
            log(
                log.INFO,
                "filter_data_for_report_of_visit: client_data type [%s]",
                client_data.type,
            )
            all_visits: Visit = Visit.query.all()
            log(
                log.INFO,
                "filter_data_for_report_of_visit: all visits count [%d]",
                len(all_visits),
            )
            visits_report = self.get_visits_for_report(all_visits, start_time, end_time)

            report_of_visits = [visit.visit_info for visit in visits_report]

            log(
                log.INFO,
                "filter_data_for_report_of_visit: report of count [%d] visits",
                len(report_of_visits),
            )

            with open("./visits_report.csv", "w", newline="") as report_file:
                report = csv.writer(report_file)
                data = [["visit", "client", "start of visit", "end of visit"]]
                for visit_report in report_of_visits:
                    visit_id = visit_report["id"]
                    full_name = (
                        visit_report["client_info"]["firstName"]
                        + " "
                        + visit_report["client_info"]["lastName"]
                    )
                    visit_start = visit_report["start_time"].strftime(
                        "%H:%M:%S %b %d %Y"
                    )
                    visit_end = visit_report["end_time"].strftime("%H:%M:%S %b %d %Y")
                    data.append(
                        [
                            visit_id,
                            full_name,
                            visit_start,
                            visit_end,
                        ],
                    )
                log(
                    log.INFO,
                    "filter_data_for_report_of_visit: create report data [%s]",
                    data,
                )
                report.writerows(data)

                log(
                    log.INFO,
                    "filter_data_for_report_of_visit: write data (count of visit in data [%d]) to csv file",
                    len(data),
                )

            return report_of_visits

    def filter_data_for_report_of_new_clients(
        self, client_data: VisitReportReq, doctor: Doctor
    ) -> List[VisitReportRes]:
        log(
            log.INFO,
            "filter_data_for_report_of_new_clients: client_data [%s]",
            client_data,
        )
        start_time = client_data.start_time
        end_time = client_data.end_time

        log(
            log.INFO,
            "filter_data_for_report_of_new_clients: start_time [%s] and end_time [%s] from client_data",
            start_time,
            end_time,
        )

        if client_data.type == "new_clients":
            log(
                log.INFO,
                "filter_data_for_report_of_new_clients: client_data type [%s]",
                client_data.type,
            )
            all_visits: Visit = Visit.query.all()
            log(
                log.INFO,
                "filter_data_for_report_of_new_clients: all visits count [%d]",
                len(all_visits),
            )
            visits_report = self.get_visits_for_report(all_visits, start_time, end_time)

            report_of_new_clients = [visit.client for visit in visits_report]

            log(
                log.INFO,
                "filter_data_for_report_of_new_clients: report of count [%d] new clients",
                len(report_of_new_clients),
            )

            with open("./new_clients_report.csv", "w", newline="") as report_file:
                report = csv.writer(report_file)

                data = [
                    [
                        "client",
                        "birthday",
                        "email",
                        "phone",
                        "state",
                        "city",
                        "address",
                        "covid_tested_positive",
                        "covid_vaccine",
                        "conditions",
                        "diseases",
                        "medications",
                        "count of visits",
                    ]
                ]

                for visit_report in report_of_new_clients:
                    full_name = visit_report.first_name + " " + visit_report.last_name
                    birthday = visit_report.birthday.strftime("%b %d %Y")
                    email = visit_report.client_info["email"]
                    phone = visit_report.phone
                    state = visit_report.state
                    city = visit_report.city
                    address = visit_report.address
                    covid_tested_positive = visit_report.covid_tested_positive
                    covid_vaccine = visit_report.covid_vaccine
                    conditions = visit_report.client_info["conditions"]
                    diseases = visit_report.client_info["diseases"]
                    medications = visit_report.client_info["medications"]
                    visits = len(visit_report.client_info["visits"])

                    data.append(
                        [
                            full_name,
                            birthday,
                            email,
                            phone,
                            state,
                            city,
                            address,
                            covid_tested_positive,
                            covid_vaccine,
                            conditions,
                            diseases,
                            medications,
                            visits,
                        ],
                    )
                log(
                    log.INFO,
                    "filter_data_for_report_of_new_clients: create report data [%s]",
                    data,
                )
                data
                report.writerows(data)

                log(
                    log.INFO,
                    "filter_data_for_report_of_new_clients: write data (count of new clients in data [%d]) to csv file",
                    len(data),
                )

            return report_of_new_clients
