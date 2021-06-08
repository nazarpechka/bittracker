from django.conf import settings

class RatesAPI:
    def __init__(self):
        self.__key = settings.RATES_API_KEY

