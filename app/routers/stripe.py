from fastapi import APIRouter, Depends, Request, Header
from fastapi_pagination import Page as BasePage, paginate

from app.services import VisitService

from app.schemas import (
    DoctorStripeSecret,
    ClientInfoStripe,
    BillingBase,
    ClientStripeSubscription,
)

from app.models import Doctor

from app.services.auth import get_current_doctor

router_stripe = APIRouter(prefix="/stripe")
Page = BasePage.with_custom_options(size=4)


@router_stripe.get("/get_secret", response_model=DoctorStripeSecret, tags=["Stripe"])
async def get_secret(doctor: Doctor = Depends(get_current_doctor)):
    """Get secret stripe keys"""
    service = VisitService()

    return service.get_secret()


@router_stripe.post("/create_stripe_session", response_model=str, tags=["Stripe"])
async def create_stripe_session(
    data: ClientInfoStripe, doctor: Doctor = Depends(get_current_doctor)
):
    """Stripe session"""
    service = VisitService()
    return service.create_stripe_session(data, doctor)


@router_stripe.post("/create_stripe_subscription", response_model=str, tags=["Stripe"])
async def stripe_subscription(
    data: ClientStripeSubscription, doctor: Doctor = Depends(get_current_doctor)
):
    """Stripe session"""
    service = VisitService()
    return service.stripe_subscription(data, doctor)


@router_stripe.post("/webhook", response_model=str, tags=["Stripe"])
async def webhook(request: Request, stripe_signature: str = Header(None)):
    """Stripe webhook"""
    service = VisitService()
    service.webhook(request, stripe_signature)
    return "ok"


@router_stripe.get(
    "/billing_history/{api_key}", response_model=Page[BillingBase], tags=["Stripe"]
)
async def get_billing_history(
    api_key: str, doctor: Doctor = Depends(get_current_doctor)
):
    """Get secret stripe keys"""
    service = VisitService()
    billing_history = service.get_billing_history(api_key, doctor)

    return paginate(billing_history)
