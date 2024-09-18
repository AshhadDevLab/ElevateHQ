from django.db import models
from django.contrib.auth.models import Permission, Group
# Create your models here.
class Subscription(models.Model):
    name = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, limit_choices_to={"content_type__app_label": "subscriptions"})
    
    class Meta:
        permissions = [
            ("advanced", "Advaned permission"),
            ("pro", "Pro permission"),
            ("basic", "Basic permission"),
        ]