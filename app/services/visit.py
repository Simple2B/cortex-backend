import datetime
from typing import List
from fastapi import HTTPException, status

import stripe
from app.schemas import (
    Doctor,
    VisitInfoHistory,
    VisitHistory,
    VisitHistoryFilter,
    DoctorStripeSecret,
    ClientInfoStripe,
    BillingBase,
)
from app.models import Client as ClientDB, Billing
from app.config import settings as config
from app.logger import log


class VisitService:
    def get_history_visit(self, api_key: str, doctor: Doctor) -> List[VisitHistory]:
        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()
        if not client:
            log(log.ERROR, "get_history_visit: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "get_history_visit: Client [%s]", client)
        visits: VisitInfoHistory = client.client_info["visits"]

        log(log.INFO, "get_history_visit: Count [%d] of visits ", len(visits))
        visits_history = []
        for visit in visits:
            if visit.end_time:
                visits_history.append(
                    {
                        "doctor_name": doctor.first_name,
                        "date": visit.date.strftime("%m/%d/%Y"),
                    }
                )

        return visits_history

    def filter_visits(
        self, data: VisitHistoryFilter, doctor: Doctor
    ) -> List[VisitHistory]:
        client: ClientDB = ClientDB.query.filter(
            ClientDB.api_key == data.api_key
        ).first()
        if not client:
            log(log.ERROR, "filter_visits: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "filter_visits: Client [%s]", client)

        visits = client.client_info["visits"]
        log(
            log.INFO,
            "filter_visits: Count of all visits [%d] for client [%s]",
            len(visits),
            client,
        )

        visits_report = []

        for visit in visits:
            if visit.end_time:
                log(
                    log.INFO,
                    "filter_visits: visit [%s] with end_time]",
                    visit,
                )
                visit_start_time = datetime.datetime.strptime(
                    visit.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
                    "%m/%d/%Y, %H:%M:%S",
                )
                log(
                    log.INFO,
                    "filter_visits: visit start_time [%s]",
                    visit_start_time,
                )
                visit_end_time = datetime.datetime.strptime(
                    visit.end_time.strftime("%m/%d/%Y, %H:%M:%S"),
                    "%m/%d/%Y, %H:%M:%S",
                )
                log(
                    log.INFO,
                    "filter_visits: visit end_time [%s]",
                    visit_end_time,
                )
                if visit_start_time >= datetime.datetime.strptime(
                    data.start_time, "%m/%d/%Y, %H:%M:%S"
                ) and visit_end_time <= datetime.datetime.strptime(
                    data.end_time, "%m/%d/%Y, %H:%M:%S"
                ):
                    visits_report.append(visit)

        if len(visits_report) > 0:

            filter_visits = [
                {
                    "doctor_name": doctor.first_name,
                    "date": visit.date.strftime("%m/%d/%Y"),
                }
                for visit in visits_report
            ]
            log(log.INFO, "filter_visits: Count of visits [%d]", len(filter_visits))

            return filter_visits
        return []

    def get_secret(self) -> DoctorStripeSecret:

        return {
            "pk_test": config.PK_TEST,
            "sk_test": config.SK_TEST,
            "cortex_key": config.CORTEX_KEY,
        }

    def create_stripe_session(self, data: ClientInfoStripe, doctor: Doctor) -> None:
        stripe.api_key = config.CORTEX_KEY
        try:
            charge = stripe.Charge.create(
                amount=data.amount,
                currency="usd",
                description=data.description,
                source="tok_visa",
                idempotency_key=data.id,
            )
            log(log.INFO, "create_stripe_session: stripe charge [%s]", charge)

            client: ClientDB = ClientDB.query.filter(
                ClientDB.api_key == data.api_key
            ).first()

            if not client:
                log(log.ERROR, "create_stripe_session: Client not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
                )

            log(log.INFO, "create_stripe_session: Client [%s]", client)

            client_billing = Billing(
                description=data.description,
                amount=data.amount / 100,
                client_id=client.id,
                doctor_id=doctor.id,
            ).save()

            log(
                log.INFO,
                "create_stripe_session: billing [%d] saved for client [%d] [%s]",
                client_billing.id,
                client.id,
                client.first_name,
            )

        except stripe.error.StripeError as error:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=str(error.args),
            )

    def get_billing_history(self, api_key: str, doctor: Doctor) -> List[BillingBase]:
        client: ClientDB = ClientDB.query.filter(ClientDB.api_key == api_key).first()

        if not client:
            log(log.ERROR, "get_billing_history: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "get_billing_history: Client [%s]", client)

        client_billings: Billing = Billing.query.filter(
            Billing.client_id == client.id
        ).all()

        log(
            log.INFO,
            "get_billing_history: Client [%s] count of billings [%d]",
            client,
            len(client_billings),
        )

        billing = []

        if len(client_billings) > 0:
            for client_billing in client_billings:
                billing.append(
                    {
                        "date": client_billing.date.strftime("%m/%d/%Y"),
                        "description": client_billing.description,
                        "amount": client_billing.amount,
                        "client_name": client.first_name + " " + client.last_name,
                        "doctor_name": doctor.first_name + " " + doctor.last_name,
                    }
                )
        if len(billing) > 0:
            return billing

        return [
            {
                "date": "",
                "description": "",
                "amount": None,
                "client_name": "",
                "doctor_name": "",
            }
        ]
