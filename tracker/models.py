from django.contrib.auth.models import User
from django.db import models

from .api.APIFactory import APIFactory
from .api.CoinMarketCap import CoinMarketCap


class Crypto(models.Model):
    """Defines cryptocurrencies which can be used in tracker"""
    symbol = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Fiat(models.Model):
    """Defines fiat currencies which can be used in tracker"""
    symbol = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Defines user account in the application"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fiat = models.ForeignKey(Fiat, on_delete=models.CASCADE, default='USD')

    def __str__(self):
        return f"{self.user} - {self.fiat}"


class Rate(models.Model):
    """Defines conversion rate between cryptocurrency and fiat"""
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    fiat = models.ForeignKey(Fiat, on_delete=models.CASCADE)
    rate = models.FloatField(null=True)

    def __str__(self):
        return f"1 {self.crypto} -> {self.rate} {self.fiat}"


class Exchange(models.Model):
    """Defines exchanges which tracker integrates with"""
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return f"{self.name}"


class ExchangeAccount(models.Model):
    """Defines a specific exchange account with API key"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    key = models.CharField(max_length=1024)
    secret = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.exchange}[{self.user.user}]"


class Balance(models.Model):
    """Defines balance of cryptocurrency user owns"""
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount} {self.crypto}"

    class Meta:
        abstract = True


class ExchangeBalance(Balance):
    """Defines balance of cryptocurrency on exchange"""
    exchange_account = models.ForeignKey(ExchangeAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.exchange_account}: {super().__str__()}"


class ManualBalance(Balance):
    """Defines balance of cryptocurrency from manual user input"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}: {super().__str__()}"


def get_user_balances(user):
    total_balances = {}
    exchange_accounts = ExchangeAccount.objects.filter(user=user)
    exchange_balances = ExchangeBalance.objects.filter(exchange_account__in=exchange_accounts)
    manual_balances = ManualBalance.objects.filter(user=user)
    balances = exchange_balances.union(manual_balances)

    user_fiat = user.fiat

    for balance in balances:
        crypto = balance.crypto
        amount = balance.amount
        try:
            rate = Rate.objects.get(crypto=crypto, fiat=user_fiat)
            amount_fiat = rate.rate * amount
        except (Rate.DoesNotExist, TypeError):
            amount_fiat = 0

        if amount is None:
            continue
        if crypto in total_balances:
            total_balances[crypto]['amount'] += amount
            total_balances[crypto]['amount_fiat'] += amount_fiat
        else:
            total_balances[crypto] = {
                'amount': amount,
                'amount_fiat': amount_fiat
            }

    return total_balances


def refresh_rates():
    cmc = CoinMarketCap()

    fiats = Fiat.objects.all()
    cryptos = Crypto.objects.all()

    for fiat in fiats:
        rates = cmc.get_crypto_rates(fiat.symbol)
        for crypto in cryptos:
            if crypto.symbol in rates:
                rate, _ = Rate.objects.get_or_create(
                    crypto=crypto,
                    fiat=fiat
                )
                rate.rate = rates[crypto.symbol]
                rate.save()


def refresh_balances():
    accounts = ExchangeAccount.objects.all()

    for account in accounts:
        api = APIFactory.create(account)
        balance = api.get_balance()

        for symbol, amount in balance.items():
            crypto, _ = Crypto.objects.get_or_create(symbol=symbol)
            exchange_balance, _ = ExchangeBalance.objects.get_or_create(exchange_account=account, crypto=crypto)
            exchange_balance.amount = amount
            exchange_balance.save()

        for exchange_balance in ExchangeBalance.objects.all():
            if exchange_balance.crypto.symbol not in balance:
                exchange_balance.delete()
