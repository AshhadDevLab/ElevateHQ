from django.contrib import admin
from .models import Subscription, UserSubscription, SubscriptionPrice

# Register your models here.
class SubscriptionPrice(admin.StackedInline):
    model = SubscriptionPrice
    extra = 0
    readonly_fields = ["stripe_id"]
    can_delete = False

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    search_fields = ["name"]
    list_filter = ["active"]
    inlines = [SubscriptionPrice]
    readonly_fields = ["stripe_id"]


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(UserSubscription)