from django.db import models
from django.contrib.auth.models import Permission, Group
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

ALLOW_CUSTOM_GROUPS = True

class Subscription(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        permissions = [
            ("advanced", "Advanced Permission"),
            ("pro", "Pro Permission"),
            ("basic", "Basic Permission"),
        ]

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscriptions = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscriptions.name}"

def user_sub_post_save(sender, instance, created, *args, **kwargs):
    print(instance)
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscriptions
    groups = subscription_obj.groups.all()
    if not ALLOW_CUSTOM_GROUPS:
        user.group.set(groups)
    else:
        subs_qs = Subscription.objects.filter(active=True).exclude(id=subscription_obj.id)
        subs_groups = subs_qs.groups.values_list("id", flat=True)
        subs_groups_set = set(subs_groups)
        # group_ids = groups.values_list("id", flat=True)
        current_groups = user.groups.all().values_list("id", flat=True)
        group_ids_set = set(group_ids)
        current_groups_set = set(current_groups) - subs_groups_set
        final_group_ids = list(group_ids_set | current_groups_set)
        user.groups.set(final_group_ids)
    
    
post_save.connect(user_sub_post_save, sender=UserSubscription)