from django.shortcuts import render
from django.http import HttpResponse

from .api.CoinMarketCap import CoinMarketCap


def index(request):
    cmc = CoinMarketCap()
    return HttpResponse(cmc.get_crypto_rates("UAH"))