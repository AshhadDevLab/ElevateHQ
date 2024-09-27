from subscriptions.models import Subscription
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print("Hello World!")
        qs = Subscription.objects.filter(active=True)
        for obj in qs:
            for group in obj.groups.all():
                group.permissions.set(obj.permissions.all())