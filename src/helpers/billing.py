import stripe
from decouple import config

DJANGO_DEBUG=config("DJANGO_DEBUG", default=False, cast=bool)
STRIPE_SECRET_KEY=config("STRIPE_SECRET_KEY", default="", cast=str)

if "sk_test" in STRIPE_SECRET_KEY and DJANGO_DEBUG:
    raise ValueError("Invalid Stripe key for production")

stripe.api_key = STRIPE_SECRET_KEY

def create_customer(name="", email="", raw=False):
    response = stripe.Customer.create(
    name="Jenny Rosen",
    email="jennyrosen@example.com",
    )
    if raw:
        return response
    return response.id