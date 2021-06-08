from django.core.management.base import BaseCommand

from tracker.models import refresh_rates

class Command(BaseCommand):
    help = 'Updates current rates for every crypto/fiat pair'

    def handle(self, *args, **options):
        refresh_rates()

