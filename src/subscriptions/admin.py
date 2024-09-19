from django.contrib import admin
from .models import Subscription, UserSubscription

# Register your models here.
admin.site.register(Subscription)
admin.site.register(UserSubscription)