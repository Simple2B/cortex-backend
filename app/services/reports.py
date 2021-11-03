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
    def filter_data_for_report(
        self, client_data: VisitReportReq, doctor: Doctor
    ) -> List[VisitReportRes]:
        log(
            log.INFO,
            "filter_data_for_report: client_data [%s]",
            client_data,
        )
        start_time = datetime.datetime.strptime(
            client_data.start_time, "%m/%d/%Y, %H:%M:%S"
        )
        end_time = datetime.datetime.strptime(
            client_data.end_time, "%m/%d/%Y, %H:%M:%S"
        )

        log(
            log.INFO,
            "filter_data_for_report: start_time [%s] and end_time [%s] from client_data",
            start_time,
            end_time,
        )

        if client_data.type == "visit":
            log(
                log.INFO,
                "filter_data_for_report: client_data type [%s]",
                client_data.type,
            )
            all_visits: Visit = Visit.query.all()
            log(
                log.INFO,
                "filter_data_for_report: all visits count [%d] for report",
                len(all_visits),
            )
            visits_report = []

            for visit in all_visits:
                if visit.start_time >= start_time and visit.end_time <= end_time:
                    visits_report.append(visit)

            report = [visit.visit_info for visit in visits_report]

            log(
                log.INFO,
                "filter_data_for_report: report [%d]",
                len(report),
            )

            return report
