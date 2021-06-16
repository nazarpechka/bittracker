import hashlib, hmac
from urllib.parse import urlencode

from tracker.api.API import API
from django.conf import settings


class Binance(API):
    def __init__(self, key, secret):
        super().__init__(key, secret)

    def get_balance(self):
        url = settings.BINANCE_URL + settings.BINANCE_WALLET
        timestamp = self._request(settings.BINANCE_URL + settings.BINANCE_TIME)["serverTime"]

        headers = {
            "X-MBX-APIKEY": self._key,
        }
        params = {
            "timestamp": timestamp
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self._secret.encode('utf-8'),
                                       query_string.encode('utf-8'),
                                       hashlib.sha256).hexdigest()

        response = self._request(url, headers, params)

        balance = {}
        for crypto in response:
            free = float(crypto["free"])
            locked = float(crypto["locked"])
            total = free + locked
            if total > settings.MIN_BALANCE:
                balance[crypto["coin"]] = total

        return balance