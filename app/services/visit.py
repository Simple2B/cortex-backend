import datetime
from typing import List
from fastapi import HTTPException, status, Request
import stripe

from app.schemas import (
    Doctor,
    VisitInfoHistory,
    VisitHistory,
    VisitHistoryFilter,
    DoctorStripeSecret,
    ClientInfoStripe,
    BillingBase,
    ClientStripeSubscription,
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

    def create_stripe_session(self, data: ClientInfoStripe, doctor: Doctor) -> str:
        stripe.api_key = config.SK_TEST
        customer = stripe.Customer.create(
            email=data.email,
        )
        log(
            log.INFO, "create_stripe_session: customer created [%s]", customer.stripe_id
        )

        charge = stripe.Charge.create(
            amount=data.amount,
            currency="usd",
            description=data.description,
            source="tok_visa",
            idempotency_key=data.id,
            receipt_email=data.email,
            # customer=customer.stripe_id,
        )
        log(log.INFO, "create_stripe_session: stripe charge [%s]", charge)

        payment_intent = stripe.PaymentIntent.create(
            amount=data.amount,
            currency="usd",
            payment_method_types=["card"],
            customer=customer.stripe_id,
        )

        payment_intent

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
            payment_method=data.id,
            status=charge["status"],
        ).save()

        log(
            log.INFO,
            "create_stripe_session: billing [%d] saved for client [%d] [%s]",
            client_billing.id,
            client.id,
            client.first_name,
        )

        return "ok"

    def stripe_subscription(
        self, data: ClientStripeSubscription, doctor: Doctor
    ) -> str:
        stripe.api_key = config.SK_TEST
        product = config.CORTEX_PRODUCT_ID

        client: ClientDB = ClientDB.query.filter(
            ClientDB.api_key == data.api_key
        ).first()

        if not client:
            log(log.ERROR, "stripe_subscription: Client not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )

        log(log.INFO, "stripe_subscription: Client [%s]", client)

        customer = stripe.Customer.create(
            description=data.name,
            email=data.email,
            payment_method=data.payment_method,
            name=data.name,
        )

        if not customer:
            log(log.ERROR, "stripe_subscription: customer didn't create")

        log(
            log.INFO,
            "stripe_subscription: created customer [%s]",
            customer.stripe_id,
        )

        price = stripe.Price.create(
            unit_amount=data.amount,
            currency="usd",
            recurring={
                "interval": data.interval.split("-")[1],
                "interval_count": data.interval.split("-")[0],
            },
            product=product,
        )

        log(
            log.INFO,
            "stripe_subscription: created price [%s]",
            price.stripe_id,
        )

        payment_method = stripe.PaymentMethod.attach(
            data.payment_method,
            customer=customer.stripe_id,
        )

        log(
            log.INFO,
            "stripe_subscription: created payment_method [%s]",
            payment_method.stripe_id,
        )

        # Set the default payment method on the customer
        stripe.Customer.modify(
            customer.stripe_id,
            invoice_settings={
                "default_payment_method": payment_method.stripe_id,
            },
        )

        quantity = int(data.interval_count) if len(data.interval_count) > 0 else 1

        subscription = stripe.Subscription.create(
            customer=customer.stripe_id,
            items=[
                {
                    "price": price.stripe_id,
                    "quantity": quantity,
                },
            ],
        )

        log(
            log.INFO,
            "stripe_subscription: created subscription [%s]",
            subscription.stripe_id,
        )

        modify_subscription = stripe.Subscription.modify(
            subscription.stripe_id,
            billing_cycle_anchor="now",
            proration_behavior="always_invoice",
        )

        log(
            log.INFO,
            "stripe_subscription: subscription [%s] modify successfully ",
            modify_subscription.stripe_id,
        )

        info_payment_method = stripe.PaymentMethod.retrieve(
            payment_method.stripe_id,
        )

        billing = Billing(
            description=data.description,
            amount=data.amount / 100,
            customer_stripe_id=customer.stripe_id,
            subscription_id=subscription.stripe_id,
            subscription_quantity=int(data.interval_count)
            if len(data.interval_count) > 0
            else 1,
            subscription_interval=data.interval.split("-")[1],
            subscription_interval_count=data.interval.split("-")[0],
            payment_method=data.payment_method,
            status=subscription["status"],
            client_id=client.id,
            doctor_id=doctor.id,
        ).save()

        log(
            log.INFO,
            "stripe_subscription: created new billing [%d] for client [%d]",
            billing.id,
            client.id,
        )

        return "ok"

    async def webhook(self, request: Request, stripe_signature: str):
        webhook_secret = config.STRIPE_WEBHOOK_SECRET
        data = await request.body()
        try:
            event = stripe.Webhook.construct_event(
                payload=data, secret=webhook_secret, sig_header=stripe_signature
            )
            event_data = event["data"]
            event_data
        except Exception as e:
            return {"error": str(e)}

        event_type = event["type"]
        if event_type == "checkout.session.completed":
            print("checkout session completed")
        elif event_type == "invoice.paid":
            print("invoice paid")
        elif event_type == "invoice.payment_failed":
            print("invoice payment failed")
        elif event_type == "charge.succeeded":
            print("charge succeeded")
        else:
            print(f"unhandled event: {event_type}")
        return {"status": "success"}

    def get_billing_history(self, api_key: str, doctor: Doctor) -> List[BillingBase]:
        stripe.api_key = config.SK_TEST
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
                payment_method = None
                if client_billing.payment_method:
                    payment_method = client_billing.payment_method

                    info_payment_method = stripe.PaymentMethod.retrieve(
                        payment_method,
                    )

                    info_payment_method

                customer_stripe_id: Billing = client_billing.customer_stripe_id
                date_next_payment_attempt = None
                paid = None
                if client_billing.subscription_id:
                    log(
                        log.INFO,
                        "get_billing_history: client subscription [%s]",
                        client_billing.subscription_id,
                    )

                    invoice = stripe.Invoice.upcoming(
                        customer=customer_stripe_id,
                    )

                    # log(
                    #     log.INFO,
                    #     "get_billing_history: subscription data [%s]",
                    #     invoice,
                    # )

                    next_payment_attempt = invoice["next_payment_attempt"]

                    date_next_payment_attempt = datetime.datetime.fromtimestamp(
                        next_payment_attempt
                    ).strftime("%m/%d/%Y")

                    # log(
                    #     log.INFO,
                    #     "get_billing_history: next payment date [%s]",
                    #     date_next_payment_attempt,
                    # )

                    paid = invoice["paid"]

                    # log(
                    #     log.INFO,
                    #     "get_billing_history: paid [%s]",
                    #     paid,
                    # )

                client_amount = str(client_billing.amount)
                pay_period = str(client_billing.subscription_interval_count)
                subscription_quantity = str(client_billing.subscription_quantity)

                billing.append(
                    {
                        "date": client_billing.date.strftime("%m/%d/%Y"),
                        "description": client_billing.description,
                        "amount": client_amount,
                        "subscription_interval": client_billing.subscription_interval,
                        "pay_period": pay_period,
                        "subscription_quantity": subscription_quantity,
                        "client_name": client.first_name + " " + client.last_name,
                        "doctor_name": doctor.first_name + " " + doctor.last_name,
                        "paid": paid,
                        "status": client_billing.status,
                        "date_next_payment_attempt": date_next_payment_attempt,
                    }
                )
        if len(billing) > 0:
            return billing

        return [
            {
                "date": "",
                "description": "",
                "amount": None,
                "subscription_interval": "",
                "pay_period": "",
                "subscription_quantity": "",
                "client_name": "",
                "doctor_name": "",
                "paid": None,
                "status": None,
                "date_next_payment_attempt": None,
            }
        ]
