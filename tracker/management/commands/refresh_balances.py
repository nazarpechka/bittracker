from django.core.management.base import BaseCommand

from tracker.models import refresh_balances

class Command(BaseCommand):
    help = 'Updates exchange balances for each user'

    def handle(self, *args, **options):
        refresh_balances()

