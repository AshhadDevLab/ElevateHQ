from django.core.management.base import BaseCommand
from subscriptions.utils import sync_subs_group_permissions

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        sync_subs_group_permissions()