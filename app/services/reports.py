import datetime
from typing import List

from app.schemas import (
    Doctor,
    VisitReportReq,
    VisitReportRes,
)
from app.models import Visit

# from app.logger import log


class ReportService:
    def filter_data_for_report(
        self, client_data: VisitReportReq, doctor: Doctor
    ) -> List[VisitReportRes]:
        start_time = datetime.datetime.strptime(
            client_data.start_time, "%m/%d/%Y, %H:%M:%S"
        )
        end_time = datetime.datetime.strptime(
            client_data.end_time, "%m/%d/%Y, %H:%M:%S"
        )

        if client_data.type == "visit":
            all_visits: Visit = Visit.query.all()
            visits_report = []

            for visit in all_visits:
                if visit.start_time >= start_time and visit.end_time <= end_time:
                    visits_report.append(visit)

            report = [visit.visit_info for visit in visits_report]

            return report
