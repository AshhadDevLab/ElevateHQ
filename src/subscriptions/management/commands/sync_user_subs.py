from typing import Any
from django.core.management.base import BaseCommand
from helpers.billing import get_customer_active_subscriptions, cancel_subscription
from customers.models import Customer
from subscriptions.utils import clear_dangling_subs

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument("--clear-dangling", action="store_true", default = False)
        
    def handle(self, *args:Any, **options: Any):
        clear_dangling = options.get("clear_dangling")
        if clear_dangling:
            clear_dangling_subs()
        