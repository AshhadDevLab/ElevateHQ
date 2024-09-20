from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from subscriptions.models import SubscriptionPrice
from helpers.billing import start_checkout_session
from django.urls import reverse
from django.conf import settings

# Create your views here.
def product_price_redirect_views(request, price_id=None, *args, **kwargs):
    request.session["checkout_subscription_price_id"] = price_id
    return redirect('stripe-checkout-start')

@login_required
def checkout_redirect_view(request):
    print(request.user)
    checkout_subscription_price_id = request.session.get("checkout_subscription_price_id")
    try:
        obj = SubscriptionPrice.objects.get(id=checkout_subscription_price_id)
    except:
        obj = None
    if checkout_subscription_price_id is None or obj is None:
        return redirect("pricing")
    customer_stripe_id = request.user.customer.stripe_id
    success_url_base = settings.BASE_URL
    success_url_path = reverse("stripe-checkout-end")
    pricing_url_path = reverse("pricing")
    success_url = f"{success_url_base}{success_url_path}?session_id="
    cancel_url = f"{success_url_base}{pricing_url_path}"
    price_stripe_id = obj.stripe_id
    url = start_checkout_session(
        customer_stripe_id,
        success_url=success_url,
        cancel_url=cancel_url,
        raw=False,
        price_stripe_id=price_stripe_id
    )
    return redirect(url)

def checkout_finalised_view(request):
    return render(request, "checkouts/finalised.html", {})