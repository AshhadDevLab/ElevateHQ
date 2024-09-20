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

def start_checkout_session(customer_id, success_url="", price_stripe_id="", raw=True, cancel_url=""):
    if not success_url.endswith("?session_id={CHECKOUT_SESSION_ID}"):
        success_url = f"{success_url}" + "?session_id={CHECKOUT_SESSION_ID}"
    response = stripe.checkout.Session.create(
    customer=customer_id,
    success_url=success_url,
    cancel_url=cancel_url,
    line_items=[{"price": price_stripe_id, "quantity": 1}],
    mode="subscription",
    )
    if raw:
        return response
    return response.url