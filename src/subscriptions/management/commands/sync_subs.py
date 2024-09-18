from typing import Any
from django.core.management.base import BaseCommand
from subscriptions.models import Subscription

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        print("Hello World!")