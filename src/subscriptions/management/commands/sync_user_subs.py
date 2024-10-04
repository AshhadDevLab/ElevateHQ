from typing import Any
from django.core.management.base import BaseCommand
from subscriptions.utils import clear_dangling_subs, refresh_active_users_subscription


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--day-start", default=0, type=int)
        parser.add_argument("--day-end", default=0, type=int)
        parser.add_argument("--days-left", default=0, type=int)
        parser.add_argument("--days_ago", default=0, type=int)
        parser.add_argument("--clear-dangling", action="store_true", default=False)

    def handle(self, *args: Any, **options: Any):
        days_left = options.get("days_left")
        days_ago = options.get("days_ago")
        day_start = options.get("day_start")
        day_end = options.get("day_end")
        clear_dangling = options.get("clear_dangling")
        if clear_dangling:
            clear_dangling_subs()
        else:
            done = refresh_active_users_subscription(
                active_only=True,
                verbose=True,
                days_ago=days_ago,
                days_left=days_left,
                day_start=day_start,
                day_end=day_end,
            )
            if done:
                print("Done")
