import stripe
from decouple import config
from .date_utils import timestamp_as_datetime

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
    if "?session_id={CHECKOUT_SESSION_ID}" not in success_url:
        if "?" in success_url:
            success_url = f"{success_url}&session_id={{CHECKOUT_SESSION_ID}}"
        else:
            success_url = f"{success_url}?session_id={{CHECKOUT_SESSION_ID}}"
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

def get_checkout_session(stripe_id, raw=True):
    response = stripe.checkout.Session.retrieve(stripe_id)
    if raw:
        return response
    return response.url

def get_subscription(stripe_id, raw=True):
    response = stripe.Subscription.retrieve(stripe_id)
    if raw:
        return response
    return response.url

def cancel_subscription(stripe_id, reason="", feedback="other", raw=True):
    response = stripe.Subscription.cancel(stripe_id, cancellation_details={"comment": reason, "feedback": feedback})
    if raw:
        return response
    return response.url

def serialize_subscription_data(subscription_response):
    status = subscription_response.status
    current_period_start = timestamp_as_datetime(subscription_response.current_period_start)
    current_period_end = timestamp_as_datetime(subscription_response.current_period_end)
    return {
        "current_period_start": current_period_start,
        "current_period_end": current_period_end,
        "status": status,
    }

def get_checkout_customer_plan(session_id):
    checkout_r = get_checkout_session(session_id, raw=True)
    customer_id = checkout_r.customer
    sub_stripe_id = checkout_r.subscription
    sub_r = get_subscription(sub_stripe_id, raw=True)
    sub_plan = sub_r.plan
    subscription_data = serialize_subscription_data(sub_r)
    
    data = {
        "customer_id": customer_id,
        "plan_id": sub_plan.id,
        "sub_stripe_id": sub_stripe_id,
        **subscription_data,
    }
    return data