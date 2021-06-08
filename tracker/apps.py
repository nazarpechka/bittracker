from django.apps import AppConfig


class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'
    verbose_name = 'Cryptocurrency portfolio tracker'

    DEFAULT_CRYPTO = 'BTC'
    DEFAULT_FIAT = 'USD'


