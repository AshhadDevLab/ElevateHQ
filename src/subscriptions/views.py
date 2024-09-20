from django.shortcuts import render
from django.urls import reverse
from subscriptions.models import SubscriptionPrice

# Create your views here.
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