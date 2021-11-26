import stripe

from app.config import settings as config

stripe.api_key = config.SK_TEST
