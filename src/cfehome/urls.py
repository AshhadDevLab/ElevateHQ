"""
URL configuration for cfehome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from checkouts.views import (
    checkout_redirect_view,
    checkout_finalised_view,
    product_price_redirect_views,
)
from .views import (
    home_view,
    about_view,
    pw_protected_view,
    user_only_view,
    staff_only_view,
)
from subscriptions.views import (
    subscriptions_price_view,
    user_subscriptions_view,
    user_subscriptions_cancel_view,
)
from landing.views import landing_page_view

urlpatterns = [
    path("", landing_page_view, name="home"),
    # path('register/', register_view),
    # path("login/", login_view),
    path(
        "checkout/sub-price/<int:price_id>/",
        product_price_redirect_views,
        name="sub-price-checkout",
    ),
    path("checkout/start/", checkout_redirect_view, name="stripe-checkout-start"),
    path("checkout/sucess/", checkout_finalised_view, name="stripe-checkout-end"),
    path("about/", about_view),
    path("hello-world/", home_view),
    path("admin/", admin.site.urls),
    path("accounts/billing/", user_subscriptions_view, name="user_subscription"),
    path(
        "accounts/billing/cancel",
        user_subscriptions_cancel_view,
        name="user_subscription_cancel",
    ),
    path("accounts/", include("allauth.urls")),
    path("protected/", pw_protected_view),
    path("protected/user-only", user_only_view),
    path("protected/staff-only", staff_only_view),
    path("profiles/", include("profiles.urls")),
    path("pricing/", subscriptions_price_view, name="pricing"),
    path("pricing/<str:interval>/", subscriptions_price_view, name="pricing"),
]
