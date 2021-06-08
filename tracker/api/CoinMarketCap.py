from django.conf import settings

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


class CoinMarketCap:
    def __init__(self):
        self.__session = Session()
        self.__base_url = settings.COINMARKETCAP_URL
        self.__headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': settings.COINMARKETCAP_KEY,
        }
        self.__session.headers.update(self.__headers)

    def __request(self, path, parameters):
        data = None
        try:
            response = self.__session.get(self.__base_url + path, params=parameters)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        return data

    def get_crypto_list(self):
        parameters = {
            'start': '1',
            'limit': '150',
        }
        response = self.__request('/cryptocurrency/map', parameters)["data"]
        cryptos = {}
        for crypto in response:
            cryptos[crypto["symbol"]] = crypto["name"]
        return cryptos

    def get_fiat_list(self):
        parameters = {
            'start': '1',
            'limit': '20',
        }
        response = self.__request('/fiat/map', parameters)["data"]
        fiats = {}
        for fiat in response:
            fiats[fiat["symbol"]] = fiat["name"]
        return fiats

    def get_crypto_rates(self, fiat):
        parameters = {
            'start': '1',
            'limit': '150',
            'convert': fiat
        }
        response = self.__request('/cryptocurrency/listings/latest', parameters)["data"]
        rates = {}
        for rate in response:
            rates[rate["symbol"]] = float(rate["quote"][fiat]["price"])
        return rates


