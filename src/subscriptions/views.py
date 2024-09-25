from django.shortcuts import render, redirect
from django.urls import reverse
from subscriptions.models import SubscriptionPrice, UserSubscription
from django.contrib.auth.decorators import login_required
from helpers.billing import get_subscription


# Create your views here.
@login_required
def user_subscriptions_view(request):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user = request.user)
    sub_data = user_sub_obj.serialize()
    if request.method == "POST":
        print("refresh sub")
        if user_sub_obj.stripe_id:
            sub_data = get_subscription(user_sub_obj.stripe_id, raw=False)
            for k,v in sub_data.items():
                setattr(user_sub_obj, k, v)
            user_sub_obj.save()
        return redirect(user_sub_obj.get_absolute_url())
    return render(request, 'subscriptions/user_detail_view.html', {"subscription": user_sub_obj})

def subscriptions_price_view(request, interval="year"):
    qs = SubscriptionPrice.objects.filter(featured=True)
    int_monthly = SubscriptionPrice.IntervalChoices.MONTHLY
    int_yearly = SubscriptionPrice.IntervalChoices.YEARLY
    url_monthly = reverse("pricing", kwargs={"interval": "month"})
    url_yearly = reverse("pricing", kwargs={"interval": "year"})
    active = int_yearly
    object_list = qs.filter(interval = int_yearly)
    if interval == int_monthly:
        active = int_monthly
        object_list = qs.filter(interval = int_monthly)
    return render(request, "subscriptions/pricing.html", {
        "object_list": object_list,
        "url_monthly": url_monthly,
        "url_yearly": url_yearly,
        "active": active,
    }) 