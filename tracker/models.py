from django.contrib.auth.models import User
from django.db import models

from .apps import TrackerConfig


class Crypto(models.Model):
    """Defines cryptocurrencies which can be used in tracker"""
    name = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.name


class Fiat(models.Model):
    """Defines fiat currencies which can be used in tracker"""
    name = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.name


class Rate(models.Model):
    """Defines conversion rate between cryptocurrency and fiat"""
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    fiat = models.ForeignKey(Fiat, on_delete=models.CASCADE)
    rate = models.FloatField()

    def __str__(self):
        return f"1 {self.crypto} -> {self.rate} {self.fiat}"


class Exchange(models.Model):
    """Defines exchanges which tracker integrates with"""
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return f"{self.name}"


class ExchangeAccount(models.Model):
    """Defines a specific exchange account with API key"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    key = models.CharField(max_length=1024)
    secret = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.exchange}[{self.user.username}]"


class Balance(models.Model):
    """Defines balance of cryptocurrency user owns"""
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    amount = models.FloatField()
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}: {super().__str__()}"


