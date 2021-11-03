import datetime
from typing import List

from app.schemas import (
    Doctor,
    VisitReportReq,
    VisitReportRes,
)
from app.models import Visit

from app.logger import log


class ReportService:
    @staticmethod
    def format_date(time):
        return datetime.datetime.strptime(time, "%m/%d/%Y, %H:%M:%S")

    def filter_data_for_report_of_visit(
        self, client_data: VisitReportReq, doctor: Doctor
    ) -> List[VisitReportRes]:
        log(
            log.INFO,
            "filter_data_for_report_of_visit: client_data [%s]",
            client_data,
        )
        start_time = self.format_date(client_data.start_time)
        end_time = self.format_date(client_data.end_time)

        log(
            log.INFO,
            "filter_data_for_report_of_visit: start_time [%s] and end_time [%s] from client_data",
            start_time,
            end_time,
        )

        if client_data.type == "visit":
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
            visits_report = []

            for visit in all_visits:
                if visit.start_time >= start_time and visit.end_time <= end_time:
                    visits_report.append(visit)

            report_of_visits = [visit.visit_info for visit in visits_report]

            log(
                log.INFO,
                "filter_data_for_report_of_visit: report of count [%d] visits",
                len(report_of_visits),
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
        start_time = self.format_date(client_data.start_time)
        end_time = self.format_date(client_data.end_time)

        log(
            log.INFO,
            "filter_data_for_report_of_new_clients: start_time [%s] and end_time [%s] from client_data",
            start_time,
            end_time,
        )

        if client_data.type == "new clients":
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
            visits_report = []

            for visit in all_visits:
                if visit.start_time >= start_time and visit.end_time <= end_time:
                    visits_report.append(visit)

            report_of_new_clients = [visit.client for visit in visits_report]

            log(
                log.INFO,
                "filter_data_for_report_of_new_clients: report of count [%d] new clients",
                len(report_of_new_clients),
            )

            return report_of_new_clients
