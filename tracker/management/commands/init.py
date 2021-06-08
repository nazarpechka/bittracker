from django.core.management.base import BaseCommand
from tracker.apps import TrackerConfig

from tracker.api.CoinMarketCap import CoinMarketCap
from tracker.models import Crypto, Fiat, Exchange


class Command(BaseCommand):
    help = 'Initializes crypto and fiat lists'

    def handle(self, *args, **options):
        cmc = CoinMarketCap()

        for symbol, name in cmc.get_crypto_list().items():
            crypto, _ = Crypto.objects.get_or_create(
                symbol=symbol,
                name=name
            )
            crypto.save()

        for symbol, name in cmc.get_fiat_list().items():
            fiat, _ = Fiat.objects.get_or_create(
                symbol=symbol,
                name=name
            )
            fiat.save()

        for name in TrackerConfig.EXCHANGES:
            exchange, _ = Exchange.objects.get_or_create(name=name)
            exchange.save()
