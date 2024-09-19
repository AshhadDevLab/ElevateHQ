import stripe
from decouple import config

DJANGO_DEBUG=config("DJANGO_DEBUG", default=False, cast=bool)
STRIPE_SECRET_KEY=config("STRIPE_SECRET_KEY", default="", cast=str)

if "sk_test" in STRIPE_SECRET_KEY and DJANGO_DEBUG:
    raise ValueError("Invalid Stripe key for production")

stripe.api_key = STRIPE_SECRET_KEY

def create_customer(name="", email="", raw=False, metadata={}):
    response = stripe.Customer.create(
    name=name,
    email=email,
    metadata=metadata
    )
    if raw:
        return response
    return response.id

def create_product(name="", raw=False, metadata={}):
    response = stripe.Product.create(
    name=name,
    metadata=metadata
    )
    if raw:
        return response
    return response.id

def create_price(currency=99.99,
            unit_amount='usd',
            recurring={"interval": "month"},
            product = None,
            metadata = {},
            raw=False):
    if product is None:
        return None
    response = stripe.Price.create(
            currency=currency,
            unit_amount=unit_amount,
            recurring=recurring,
            product = product,
            metadata = metadata
            )
    if raw:
        return response
    return response.id