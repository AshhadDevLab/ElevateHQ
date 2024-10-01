from helpers.billing import get_customer_active_subscriptions, cancel_subscription, get_subscription
from customers.models import Customer
from subscriptions.models import UserSubscription, Subscription, SubscriptionStatus
from django.db.models import Q

def refresh_active_users_subscription(user_ids= None):
    qs = UserSubscription.objects.all()
    active_qs_lookup = (
        Q(status= SubscriptionStatus.ACTIVE) | 
        Q(status= SubscriptionStatus.TRIALING)
    )
    qs = qs.filter(active_qs_lookup)
    if isinstance(qs, list):
        qs = qs.filter(user_id__in= user_ids)
    elif isinstance(user_ids, int):
        qs = qs.filter(user_id__in= [user_ids])
    elif isinstance(user_ids, str):
        qs = qs.filter(user_id__in= [user_ids])
    
    complete_count= 0
    qs_count= qs.count( )
    
    for obj in qs:
        if obj.stripe_id:
            sub_data= get_subscription(obj.stripe_id, raw=False)
            for k, v in sub_data.items():
                setattr(obj, k, v)
            obj.save()
            complete_count += 1
    return complete_count ==  qs_count

def clear_dangling_subs():
    qs = Customer.objects.filter(stripe_id__isnull = False)
    for customer_obj in qs:
        user = customer_obj.user
        customer_stripe_id = customer_obj.stripe_id
        print(f"Sync {user} - {customer_stripe_id} subs and remove old ones")
        subs = get_customer_active_subscriptions(customer_stripe_id)
        for sub in subs:
            existing_user_subs_qs = UserSubscription.objects.filter(stripe_id__iexact = f"{sub.id}".strip())
            if existing_user_subs_qs.exists():
                continue
            cancel_subscription(sub.id, reason="Dangling active subscription", cancel_at_period_end=False)
            print(sub.id, existing_user_subs_qs.exists())

def sync_subs_group_permissions():
    qs = Subscription.objects.filter(active=True)
    for obj in qs:
        sub_perms = obj.permissions.all()
        for group in obj.groups.all():
            group.permissions.set(sub_perms)
        