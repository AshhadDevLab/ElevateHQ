from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from subscriptions.models import SubscriptionPrice, Subscription, UserSubscription
from helpers.billing import start_checkout_session, get_checkout_session, get_subscription, get_checkout_customer_plan
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
User = get_user_model()

# Create your views here.
def product_price_redirect_views(request, price_id=None, *args, **kwargs):
    request.session["checkout_subscription_price_id"] = price_id
    return redirect('stripe-checkout-start')

@login_required
def checkout_redirect_view(request):
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
    print(success_url_path)
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
    session_id = request.GET.get("session_id")
    customer_id, plan_id = get_checkout_customer_plan(session_id)
    price_qs = SubscriptionPrice.objects.filter(stripe_id=plan_id)
    try:
        sub_obj = Subscription.objects.get(subscriptionprice__stripe_id=plan_id)
    except:
        sub_obj = None
    
    try:
        user_obj = User.objects.get(customer__stripe_id=customer_id)
    except:
        user_obj = None
    
    _user_sub_exists = False
    try:
        _user_sub_obj = UserSubscription.objects.get(user=user_obj)
        _user_sub_exists = True
    except UserSubscription.DoesNotExist:
        _user_sub_obj = UserSubscription.objects.create(user=user_obj, subscriptions=sub_obj)
    except:
        _user_sub_obj = None
    if None in [user_obj, _user_sub_obj, sub_obj]:
        return HttpResponseBadRequest("There was an error with your account, please contact us.")
    if _user_sub_exists:
        _user_sub_obj.subscriptions = sub_obj
        _user_sub_obj.save()    
    context = {}
    return render(request, "checkout/success.html", context)